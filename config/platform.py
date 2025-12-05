
class Platform:
    hua_ren_video_info_re = ""
    hai_tu_video_info_re = ""

class HuaRen:
    _m3u8_from = ""
    _m3u8_from_url = ""

    @property
    def m3u8_from(self):
        return self._m3u8_from.split(",")

    @m3u8_from.setter
    def m3u8_from(self, value):
        self._m3u8_from = value

    @property
    def m3u8_from_url(self):
        return self._m3u8_from_url.split(",")

    @m3u8_from_url.setter
    def m3u8_from_url(self, value):
        self._m3u8_from_url = value
