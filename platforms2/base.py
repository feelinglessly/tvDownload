import os
import threading
import time
from urllib.parse import urlparse

from decrypt.decrypt import DecryptTs
from download.download import M3u8Downloader
from ffmpeg_ctrl.ffmpeg_ctrl import FfmpegVideo
from platforms2.itype import Videos
from tools import req
from stores.stores import get_store


class VideoSpider:
    video = None

    def __init__(self, ctrl_uuid, host, link, addr, auto_next, max_reset):
        self.ctrl_uuid = ctrl_uuid
        self.host = host
        self.link = link
        self.addr = addr
        self.auto_next = auto_next != 0
        self.MAX_RESET = max_reset
        self.check_args()

    def check_args(self):
        if not self.link.startswith(self.host):
            print(f"不支持的网站{self.link} 只支持{self.host}域名，将会修改后尝试")
            self.host = urlparse(self.link)
            return


class Scheduler(VideoSpider):
    downloader = None
    videos_directory = []
    auto_remove_ts = True
    cancel = False
    def __init__(self, ctrl_uuid, host, link, addr, auto_next, max_reset=5, max_ts_num=-1, max_thread_num=3, auto_remove_ts=True):
        """
        :param ctrl_uuid: 调度器的 uuid
        :param host: 域名会验证域名和first_url是否匹配，因为不同的平台会调用不同的子类
        :param link: 下载的视频地址
        :param addr: 下载后存放位置，必须每一个电视剧单独存放
        :param auto_next: 是否自动下一集
        :param max_reset: 每一集下载的最大重试次数
        :param max_ts_num: 最大ts数量，理论上不应该设置这个
        :param max_thread_num: ts下载的最大并发数
        :param auto_remove_ts: 是否自动删除ts文件
        """
        super().__init__(ctrl_uuid, host, link, addr, auto_next, max_reset)
        self.with_downloader(M3u8Downloader(max_ts_num, max_thread_num)) # 设置默认的下载器
        self.auto_remove_ts = auto_remove_ts

    def with_downloader(self, downloader):
        """
        修改下载器
        :param downloader: 下载器 M3u8Downloader或者他的子类
        :return:
        """
        self.downloader = downloader

    # make_directory 在存放位置创建文件夹，并且验证文件是不是存在
    def make_directory(self, video_name):
        """
        创建文件夹
        :param video_name: 名称
        :return:
        """
        directory = f"{self.addr}{os.path.sep}{video_name}"
        if os.path.exists(directory) and os.path.isdir(directory):
            return directory
        try:
            os.mkdir(directory)
        except NotImplementedError:
            raise NotImplementedError
        print("创建文件夹成功: ", directory)

        return directory

    @staticmethod
    def video_info(addr):
        """
        获得一个视频信息的类，这样做是为了不同平台可以用同样的方法
        :param addr:
        :return:
        """
        return Videos(addr)

    def ffmpeg_merge(self, directory, output_name, prefix="", suffix="mp4"):
        """
        合并视频
        :param directory: 视频位置文件夹
        :param output_name: 输出名和命名相关
        :param prefix: 匹配前缀
        :param suffix: 匹配后缀
        :return:
        """
        output_name = f"{output_name}.{suffix}"
        print("合并视频：", output_name)
        if output_name in os.listdir(self.addr):
            print(f"已存在{output_name}, 跳过。")
            return
        ff = FfmpegVideo(directory, prefix)
        ff.merge_to_mp4(output_name, self.addr)
        if self.auto_remove_ts:
            ff.remove_ts_files()

    def download(self, video: Videos, addr, auto_next):
        """
        调度集数
        :param video: 视频对象 Videos
        :param addr: 存放地址
        :param auto_next: 是否自动下一集
        :return:
        """
        if self.cancel:
            return

        if video is None:
            return
        get_store().set_video_name(self.ctrl_uuid, video.name)
        m3u8_url = video.get_m3u8_url()
        if m3u8_url == "":
            return
        output_name = video.get_output_name()
        thread = None
        if f"{output_name}.mp4" not in os.listdir(self.addr):
            directory = self.make_directory(output_name)
            # 上报
            get_store().set_nid(self.ctrl_uuid, video.video_nid)
            # 下载剧集
            ts_files, done, ts_key = self.downloader.m3u8_download(
                m3u8_url,
                directory
            )
            dt = DecryptTs(
                key_b=video.get_ts_key(ts_key),
            )
            # 解密
            for ts_file in ts_files:
                dt.decrypt(ts_file, ts_file)

            thread = threading.Thread(target=self.ffmpeg_merge, args=(directory, output_name), daemon=True)
        # if not done or self.cancel:
        if self.cancel:
            # 没下载完或者放弃了就不合并
            return
        if thread is not None:
            thread.start()
        # 处理自动下载
        if auto_next:
            print("处理下集。。。。")
            self.download(video.next(), addr, auto_next)
        if thread is not None:
            thread.join()

    def run(self):
        videos = self.video_info(self.link)
        self.downloader.with_ts_to_url(videos.get_ts_url)
        self.download(videos, self.link, self.auto_next)

    def reset(self):
        self.cancel = False
        self.downloader.reset()

    def stop(self):
        """
        停止程序，但是要等正在运行的线程执行完毕
        :return:
        """
        print("Scheduler stop")
        self.cancel = True
        self.downloader.stop()