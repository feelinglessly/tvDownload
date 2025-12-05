import json
import re

from platforms.base import Scheduler, VideoInfo

import ssl

from tools import req
from tools.path import path_join, url_join
from config import get_config

ssl._create_default_https_context = ssl._create_unverified_context

class HaiTuVideoInfo(VideoInfo):

    def get_info(self):
        findall = re.findall(get_config().platform.hai_tu_video_info_re, self.html)
        if len(findall) > 0:
            self.info = json.loads(findall[0][16: -9])

    @staticmethod
    def get_ts_url(link, string):
        """
        :param link: m3u8地址
        :param string: ts名
        :return:
        """
        pre_url = "/".join(link.split("/")[:-1])
        return url_join(pre_url, string)

    def get_m3u8_url(self):
        url = super().get_m3u8_url()
        m3u8_index = req.get(url)  # m3u8文件
        index = ""
        for i in m3u8_index.text.split("\n"):
            if not i.startswith("#") and (i.endswith("index.m3u8") or i.endswith("mixed.m3u8")):
                index = i
        m3u8_url = url_join("/".join(url.split("/")[:-1]), index)
        return m3u8_url


class HaiTuScheduler(Scheduler):
    @staticmethod
    def video_info(html):
        return HaiTuVideoInfo(html)


if __name__ == '__main__':
    spider = HaiTuScheduler(
        "https://www.haitu.xyz1",
        "https://www.haitu.xyz/vodplay/202942-7-2.html",
        "/Users/zcg/Projects/output/videos/yyqjw",
        1,
        5,
        3
    )
    spider.run()
