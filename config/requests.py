
class RequestMixin(object):
    _verify = True # 是否验证证书

    @property
    def verify(self):
        """
        是否验证证书
        :return: bool
        """
        return self._verify

    @verify.setter
    def verify(self, value):
        self._verify = value






