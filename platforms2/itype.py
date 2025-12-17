import json
import os
import re
import time

from tools import req
from tools.nuxt import paras_nuxt_data
from tools.path import url_join


class Videos:
    html = ""
    ts_key = b""
    ts_iv = b""


    line_source_name = "" # 播放线路
    link = "" # 视频地址

    name = ""
    director = ""
    performer = ""
    description = ""
    remark = ""
    tags = ""
    years = ""
    upCount = ""
    language = ""
    cover = ""
    area = ""

    _video_list = [] # 视频地址列表

    # 下面三项每个视频变化
    video_info = dict()
    video_nid = "" # 视频级数
    video_addr = "" # m3u8地址
    video_index = 0 # 当前的 m3u8_url 处于lines的第几个位
    _m3u8_url = "" # 真实的 m3u8 地址 有可能是从一个m3u8获得另一个

    def __init__(self, link):
        """
        link: 视频地址
        """
        self.link = link
        self.get_video_html(link)
        self.get_info()

    def get_info(self):
        pass

    def get_video_html(self, link):
        index_url = f"{link}".strip()
        print(f"从视频地址：{index_url}中获得html")
        res = req.get(index_url, verify=True)
        self.html = res.text

    def next(self):
        """
        用此方法得到下一级
        """
        return self


    @staticmethod
    def get_ts_url(link, string):
        """
        :param link: m3u8地址
        :param string: ts名
        :return:
        """
        if string.startswith("http"):
            return string
        pre_url = "/".join(link.split("/")[:-1])
        ts_name = os.path.basename(string)
        return url_join(pre_url, ts_name)

    def get_iv(self):
        """获得ts加密的密钥"""
        return bytes([0] * 16)   # AES-128的IV为16字节,

    def get_ts_key(self, key_url=""):
        """获得ts加密的密钥"""
        if self.ts_key != b'':
            return self.ts_key
        if key_url == "":
            return self.ts_key
        ts_key = req.get(key_url).content
        print("ts_key:", req.get(key_url).text)
        self.ts_key = ts_key
        return ts_key

    def get_m3u8_url(self):
        return self.video_addr

    def get_output_name(self):
        """
        合并后名称，非原始数据
        :return:
        """
        # return f"{self.name}{self.video_nid}" # 中文合并的时候有问题
        s = ""
        for i in self.video_nid:
            if i.isdigit():
                s += i
        if s.isdigit():
            return s
        return 0










