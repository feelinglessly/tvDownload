import os
from urllib.parse import urljoin


def path_join(p1, p2):
    return f"{p1}{os.path.sep}{p2}".replace(f"{os.path.sep}{os.path.sep}", os.path.sep).replace(
        f"{os.path.sep}{os.path.sep}{os.path.sep}", os.path.sep)

def url_join(url1, url2):
    if url1.endswith("/"):
        url1 = url1[:-1]
    if  url2.startswith("/"):
        url2 = url2[1:]
    return f"{url1}/{url2}"