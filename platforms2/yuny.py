import json
import pprint
import re
import ssl

from platforms2.base import Scheduler
from platforms2.itype import Videos
from tools import req
from tools.nuxt import paras_nuxt_data
from tools.path import path_join, url_join, url_stirp_join

ssl._create_default_https_context = ssl._create_unverified_context

class YunYVideoInfo(Videos):
    def get_info(self):
        data = paras_nuxt_data(self.html)
        for k, vd in data.get("ShallowReactive").get("data").items():
            select_id = 0
            selects = dict()
            for kk, vv in vd.items():
                if kk == "playSelectItem":
                    select_id = vv.get("id")
                if kk == "playDetail":
                    detail = vv.get("playDetail")
                    self.area = detail.get("area")
                    self.language = detail.get("language")
                    self.cover = detail.get("cover")
                    self.name = detail.get("name")
                    self.description = detail.get("description")
                    self.director = detail.get("director")
                    self.remark = detail.get("remark")
                    self.tags = detail.get("tags")
                    self.years = detail.get("years")
                    self.upCount = detail.get("upCount")
                    lines = detail.get("lines")
                    for line in lines:
                        selects[line.get("lineSourceName")] = line.get("selects")
                for source_name, videos in selects.items():
                    for idx, video in enumerate(videos):
                        if video.get("id") == select_id:
                            self.video_addr = video.get("resource")
                            self._video_list = videos
                            self.video_index = idx
                            self.line_source_name = source_name
                            self.video_nid = video.get("series")
                            self.video_info = video

    def next(self):
        """
        用此方法得到下一级
        """
        next_video_index = self.video_index + 1
        if next_video_index >= len(self._video_list):
            return None
        self.video_index = next_video_index
        self.video_info = self._video_list[self.video_index]
        self.video_nid = self.video_info.get("series")
        self.video_addr = self.video_info.get("resource")
        return self

    @staticmethod
    def get_ts_url(link, string):
        """
        :param link: m3u8地址
        :param string: ts名
        :return:
        """
        return url_stirp_join(link, string)

    def get_m3u8_url(self):
        m3u8_index = req.get(self.video_addr)  # m3u8文件
        index = ""
        for i in m3u8_index.text.split("\n"):
            if not i.startswith("#") and ("index.m3u8" in i or "mixed.m3u8" in i):
                index = i
        if index != "":
            m3u8_url = url_stirp_join(self.video_addr, index)
        else:
            m3u8_url = self.video_addr
        self._m3u8_url = m3u8_url
        return m3u8_url

    def get_iv(self):
        """获得ts加密的密钥"""
        return bytes([0] * 16)   # AES-128的IV为16字节,

    def get_ts_key(self, url=""):
        """获得ts加密的密钥"""
        if url == "":
            return self.ts_key
        key_url = ""
        if url != "":
            key_url = url_stirp_join(self._m3u8_url, url)
        ts_key = req.get(key_url).content
        self.ts_key = ts_key
        return ts_key


class YunYScheduler(Scheduler):
    @staticmethod
    def video_info(link):
        return YunYVideoInfo(link)


if __name__ == '__main__':
    import platform
    from config import init_config, set_verify, get_config
    system = platform.system()
    if system == 'Windows':
        f = "../config.yaml"
    else:
        f = "../mac_config.yaml"
    init_config(f)
    spider = YunYScheduler(
        "https://www.yuny.tv/",
        "https://www.yuny.tv/videoPlayer/166263716?detailId=203819",
        r"E:\project\watch\videos\yyqjw2",
        1,
        5,
        3
    )
    spider.run()
