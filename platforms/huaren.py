import json
import os.path
import pprint
import re

from config import get_config
from platforms.base import Scheduler, VideoInfo

import ssl

from tools import req
from tools.path import path_join, url_join, url_stirp_join

ssl._create_default_https_context = ssl._create_unverified_context

class HuaRenVideoInfo(VideoInfo):
    def get_info(self):
        findall = re.findall(get_config().platform.hua_ren_video_info_re, self.html)
        if len(findall) > 0:
            self.info = json.loads(findall[0][16: -9])
        pprint.pprint(self.info)

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
        return super().get_iv()

    def get_ts_key(self, key_url=""):
        """获得ts加密的密钥"""
        if self.ts_key != b'':
            return self.ts_key
        if key_url == "":
            m3u8_url = self.get_m3u8_url()
            key_url = m3u8_url.replace("/".join(m3u8_url.split('/')[-2:]), "ts.key")
        ts_key = req.get(key_url).content
        self.ts_key = ts_key
        return ts_key

    def get_m3u8_url(self):
        if self.m3u8_url != "":
            return self.m3u8_url
        url = super().get_m3u8_url()
        if self.get_from() in get_config().HuaRen.m3u8_from_url:
            url = f"https://www.aidy.cc/m3u8.php?url={url}"
        m3u8_index = req.get(url)  # m3u8文件
        index = ""
        for i in m3u8_index.text.split("\n"):
            if not i.startswith("#") and (i.endswith("index.m3u8") or i.endswith("mixed.m3u8")):
                index = i
        if index != "":
            # m3u8_url = url_join("/".join(url.split("/")[:-1]), index)
            # urls = url.split("/")[:-1]
            # for i in range(0, len(index.split("/"))):
            #     if index.split("/")[i] in urls:
            #         continue
            #     m3u8_url = url_join("/".join(urls), "/".join(index.split("/")[i:]))
            #     break
            m3u8_url = url_stirp_join(url, index)
        else:
            m3u8_url = url
        self.m3u8_url = m3u8_url
        return m3u8_url


class HuaRenScheduler(Scheduler):
    @staticmethod
    def video_info(html):
        return HuaRenVideoInfo(html)


if __name__ == '__main__':
    spider = HuaRenScheduler(
        "https://huarw.com/",
        "https://huarw.com/play/340399-5-5.html",
        "/Users/zcg/Projects/output/videos/huaren",
        1,
        5,
        3
    )
    spider.run()
