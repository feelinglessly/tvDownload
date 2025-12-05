import json
import os
import re
import threading

import requests

from decrypt.decrypt import DecryptTs
from download.download import M3u8Downloader
from ffmpeg_ctrl.ffmpeg_ctrl import FfmpegVideo
from tools import req
from tools.path import path_join, url_join
from urllib.parse import urlparse


class VideoInfo:
    """从网页中拿到视频的基本信息"""
    html = ""
    info = dict()
    m3u8_url = ""
    ts_key = b''

    def __init__(self, html):
        self.html = html
        self.get_info()

    def get_info(self):
        findall = re.findall(r"var player_aaaa={.*?}</script>", self.html)
        if len(findall) > 0:
            self.info = json.loads(findall[0][16: -9])

    def get_from(self):
        return self.info.get("from")

    def get_m3u8_url(self):
        """获得m3u8的地址"""
        return self.info.get("url")

    def get_ts_key(self, ts_key):
        """获得ts加密的密钥"""
        return b""

    def get_iv(self):
        """获得ts加密的密钥"""
        return bytes([0] * 16)   # AES-128的IV为16字节,

    def get_link(self):
        """
        获得视频地址 不包含域名
        :return:
        """
        return self.info.get("link")

    @staticmethod
    def get_ts_url(link, string):
        """
        :param link: m3u8地址
        :param string: ts名
        :return:
        """
        pre_url = "/".join(link.split("/")[:-1])
        return url_join(pre_url, string)

    def get_next_link(self):
        """
        下一集link
        :return:
        """
        return self.info.get("link_next", "")

    def get_video_name(self):
        return self.info.get("vod_data", dict()).get("vod_name")  # 片名

    def get_nid(self):
        return self.info.get("nid", 1)  # 当前集数

    def get_output_name(self):
        """
        合并后名称，非原始数据
        :return:
        """
        # return f"{self.get_video_name()}第{self.get_nid()}集" # 中文合并的时候有问题
        return f"no{self.get_nid()}"


class VideoSpider:
    """拿到视频"""
    def __init__(self, host, first_url, addr, auto_next, max_reset=5):
        """
        :param host: 网站域名
        :param first_url: 第一集的路由
        :param addr: 存放位置
        :param auto_next: 是否自动下载下一集
        :param max_reset: 每一集下载的最大重试次数
        """
        self.host = host
        self.first_url = first_url
        self.addr = addr
        self.auto_next = auto_next != 0
        self.MAX_RESET = max_reset
        self.check_args()

    # check_args 检查参数是否符合条件
    def check_args(self):
        if not self.first_url.startswith(self.host):
            print(f"不支持的网站{self.first_url} 只支持{self.host}域名，将会修改后尝试")
            self.host = urlparse(self.first_url)
            return

    def get_video_html(self, link, run_num):
        index_url = f"{self.host}{link}".strip()
        if run_num == 1:
            # 防止电影里的link不准确
            index_url = self.first_url
        print(f"从视频地址：{index_url}中获得html")
        res = req.get(index_url, verify=True)
        return res.text



class Scheduler(VideoSpider):
    downloader = None
    videos_directory = []
    auto_remove_ts = True
    cancel = False
    def __init__(self, host, first_url, addr, auto_next, max_reset=5, max_ts_num=-1, max_thread_num=3, auto_remove_ts=True):
        """
        :param host: 域名会验证域名和first_url是否匹配，因为不同的平台会调用不同的子类
        :param first_url: 视频网站的地址
        :param addr: 下载后存放位置，必须每一个电视剧单独存放
        :param auto_next: 是否自动下一集
        :param max_reset: 每一集下载的最大重试次数
        :param max_ts_num: 最大ts数量，理论上不应该设置这个
        :param max_thread_num: ts下载的最大并发数
        :param auto_remove_ts: 是否自动删除ts文件
        """
        super().__init__(host, first_url, addr, auto_next, max_reset)
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
    def video_info(html):
        """
        获得一个视频信息的类，这样做是为了不同平台可以用同样的方法
        :param html:
        :return:
        """
        return VideoInfo(html)

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

    def download(self, link, addr, auto_next, reset_count=0, run_num=1):
        """
        调度集数
        :param link: 视频地址（不包含域名）m3u8 地址
        :param addr: 存放地址
        :param auto_next: 是否自动下一集
        :param reset_count: 重试次数
        :param run_num: 运行次数
        :return:
        """
        print("==============================================")
        if self.cancel:
            return
        html = self.get_video_html(link, run_num)
        video_info = self.video_info(html)
        output_name = video_info.get_output_name()
        directory = self.make_directory(output_name)
        # 下载剧集

        ts_files, done, ts_key = self.downloader.m3u8_download(
            video_info.get_m3u8_url(),
            directory
        )
        print("ssss", ts_files)
        dt = DecryptTs(
            key_b=video_info.get_ts_key(ts_key),
        )

        # 解密
        for ts_file in ts_files:
            dt.decrypt(ts_file, ts_file)

        if not done or self.cancel:
            # 没下载完或者放弃了就不合并
            return

        thread = threading.Thread(target=self.ffmpeg_merge, args=(directory, output_name), daemon=True)
        thread.start()
        # 处理自动下载
        if auto_next:
            print("处理下集。。。。")
            next_link = video_info.get_next_link()
            if next_link != "":
                self.download(next_link, addr, auto_next, 0, run_num + 1)
            else:
                print("下一集地址为空，判断是否重试")
                new_link = video_info.get_link()
                if new_link == "":
                    if reset_count <= self.MAX_RESET:
                        self.download(link, addr, auto_next, reset_count + 1, run_num + 1)
                        print(f"重试第{reset_count + 1}次")
        thread.join()

    def run(self):
        # 需要最初的link作为驱动
        html = self.get_video_html("", 1)
        video_info = self.video_info(html)
        self.downloader.with_ts_to_url(video_info.get_ts_url)
        self.download(video_info.get_link(), self.addr, self.auto_next)

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


