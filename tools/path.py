import os
from urllib.parse import urljoin


def path_join(p1, p2):
    return f"{p1}{os.path.sep}{p2}".replace(f"{os.path.sep}{os.path.sep}", os.path.sep).replace(
        f"{os.path.sep}{os.path.sep}{os.path.sep}", os.path.sep)

def url_join(url1, url2):
    """
    url1+url2
    """
    if url2.startswith("http"):
        return url2
    if url1.endswith("/"):
        url1 = url1[:-1]
    if  url2.startswith("/"):
        url2 = url2[1:]
    return f"{url1}/{url2}"


def url_stirp_join(url1, url2):
    """
    合并（url1+url2）两个路由地址, 去掉 url1 的最后部分，同时去重中间相同的部分
    """
    if url2.startswith("http"):
        return url2
    urls = url1.split("/")[:-1]
    for i in range(0, len(url2.split("/"))):
        if url2.split("/")[i] in urls:
            continue
        return url_join("/".join(urls), "/".join(url2.split("/")[i:]))
    return url_join("/".join(url1.split("/")[:-1]), url2)
