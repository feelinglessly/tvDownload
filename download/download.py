import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from tools import req
from tools.path import path_join, url_join


def get_ts_url(link, string):
    """
    :param link: m3u8地址
    :param string: ts名
    :return:
    """
    pre_url = "/".join(link.split("/")[:-1])
    ts_name = os.path.basename(string)
    return url_join(pre_url, ts_name)

class MakeTsUrlByM3u8:
    def __call__(self, link, string):
        pre_url = "/".join(link.split("/")[:-1])
        ts_name = os.path.basename(string)
        return url_join(pre_url, ts_name)


class M3u8Downloader(object):
    """
    根据m3u8地址下载一个完整的视频ts文件
    """
    reset_downloader_num = 5
    ts_to_url = get_ts_url
    max_ts_num = -1
    max_thread_num = 3
    futures = []
    stop_event = threading.Event()
    def __init__(self, max_ts_num=-1, max_thread_num=3):
        """
        :param max_ts_num: 最多下载多少个ts文件就停止
        :param max_thread_num: 线程池最大容量
        """
        self.max_ts_num = max_ts_num
        self.max_thread_num = max_thread_num
        self.futures = []

    def new_thread_pool(self):
        return ThreadPoolExecutor(self.max_thread_num)

    def with_ts_to_url(self, ts_to_url):
        """
        :param ts_to_url: 根据m3u8的地址和ts名称来获得ts地址的方法，每个平台可能不一样
        :return:
        """
        self.ts_to_url = ts_to_url

    # m3u8_download url: m3u8.index
    def m3u8_download(self, m3u8_url, path):
        """
        根据m3u8地址下载ts视频
        :param m3u8_url: m3u8地址
        :param path: 存放位置
        :return:
        """
        print(f"根据m3u8地址下载：m3u8地址：{m3u8_url}, 存放位置：{path}")
        ts_index = req.get(m3u8_url)  # ts文件集合
        ts_map = dict()  # ts 地址集合
        ts_key = ""
        sp = "\r\n" if "\r" in  ts_index.text else "\n"
        for i in ts_index.text.split(sp):
            if "#EXT-X-KEY" in i:
                ts_key = i.split(",")[1].split('URI="')[1][:-1]
            if not i.startswith("#") and i.endswith(".ts"):
                ts_map[os.path.basename(i)] = self.ts_to_url(m3u8_url, i)

        if self.stop_event.is_set():
            # 提前终止
            return None
        with self.new_thread_pool() as pool:
            num = 1
            self.futures = []
            for ts_name, ts_url in ts_map.items():
                if num > self.max_ts_num > 0:
                    break
                output_name = f"{num}_{ts_name}"
                output = path_join(path, output_name)
                num += 1
                if output_name in os.listdir(path):
                    print(f"已存在{output}, 跳过。")
                    continue
                self.futures.append(pool.submit(req.download_video, ts_url, output))
        print("m3u8_download：：：", ts_key)
        ts_files, done = self.check()
        return ts_files, done, ts_key

    def check(self):
        res = []
        i = 1
        for future in self.futures:
            if future.cancelled():
                continue
            if future.exception():
                print(f"{i}/{len(self.futures)}")
                i+=1
                continue
            if future.done():
                res.append(future.result())
        print("m3u8_download：：：check", len(res) == len(self.futures))
        return res, len(res) == len(self.futures)

    def reset(self):
        self.stop_event.clear()

    def stop(self):
        print("M3u8Downloader stop")
        self.stop_event.set()
        i = 1
        for future in self.futures:
            print("M3u8Downloader stop：", i, "/", len(self.futures),
                  "，status：", future.done())
            if not future.done():
                future.cancel()
            print("M3u8Downloader stop：", i, "/", len(self.futures),
                  "，status：", future.done())
            i += 1

