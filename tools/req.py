import socket
import time
from contextlib import contextmanager

import requests
import wget

from config import get_config
from tools.retry import retry, call_time
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

@call_time("req.get")
@retry(nums=5)
def get(url, params=None, verify=None):
    if params is None:
        params = dict()
    return requests.get(
        url, params=params, timeout=10,
        verify=get_config().verify if verify is None else verify,
        headers={'User-Agent': get_config().common.USER_AGENT}
    )


@contextmanager
def temporary_timeout(timeout):
    """临时修改socket超时的上下文管理器"""
    original = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        yield
    finally:
        socket.setdefaulttimeout(original)  # 确保还原


@call_time("download_video")
@retry(nums=5)
def download_video(url, out):
    with temporary_timeout(30):
        wget.download(url, out)
        time.sleep(2)
    return out





