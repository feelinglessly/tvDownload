import yaml

from config.app import App
from config.common import Common
from config.platform import Platform, HuaRen
from config.requests import RequestMixin


class Config(RequestMixin):
    config = dict()
    def __init__(self, f=None):
        if f is None:
            return
        self.common = Common()
        self.platform = Platform()
        self.app = App()
        self.HuaRen = HuaRen()

        self.init_config(f)
    def init_config(self, f):
        with open(f, encoding="utf-8") as f:
            conf = yaml.safe_load(f)
        for k, v in self.__dict__.items():
            try:
                c = conf.get(k, None)
                if c is not None:
                    for kk, vv in c.items():
                        setattr(v, kk, vv)
            except AttributeError as e:
                raise e

_config = Config()

def get_config():
    return _config

def set_verify(verify=None):
    global _config
    if verify is not None:
        _config.verify = verify

def init_config(f="../config.yaml"):
    """
    :param f: yaml config file
    :param verify: 是否验证证书
    :return:
    """
    global _config
    _config = Config(f)
    # if verify is not None:
    #     _config.verify = verify
