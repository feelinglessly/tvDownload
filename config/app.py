class App(object):
    add_button_text = "添加"
    start_button_text = "开始下载"
    stop_button_text = "暂停下载"
    #
    platform_label = "选择平台："
    _platform_radios =  "海兔,华人"
    platform_clicked =  "华人"
    platform_tips = "不同选项使用不同的下载器，所以网址和平台必须对应"
    #
    verify_label = "验证证书："
    _verify_radios = "是,否"
    verify_clicked = "否"
    verify_tips = "选择否有被劫持风险，但是华人必须选否才可下载"
    #
    auto_next_label = "自动下一集："
    _auto_next_radios = "是, 否"
    auto_next_clicked = "否"
    auto_next_tips = "自动下载下一集"

    #
    url_line_label = "输入网址："
    url_line_placeholder = "https: // www.example.com / a / b"

    #
    host_line_label = "网站地址："
    host_line_placeholder = "htt: // www.example.com"

    #
    file_label = "存放位置："
    file_placeholder = "请选择文件夹..."

    _max_reset = 5
    _max_ts_num = -1
    _max_thread_num = 5
    _auto_remove_ts = 1


    @property
    def platform_radios(self):
        return self._platform_radios.split(",")

    @platform_radios.setter
    def platform_radios(self, value):
        self._platform_radios = value

    @property
    def verify_radios(self):
        return self._verify_radios.split(",")

    @verify_radios.setter
    def verify_radios(self, value):
        self._verify_radios = value

    @property
    def auto_next_radios(self):
        return self._auto_next_radios.split(",")

    @auto_next_radios.setter
    def auto_next_radios(self, value):
        self._auto_next_radios = value

    @property
    def max_reset(self):
        return self._max_reset

    @max_reset.setter
    def max_reset(self, value):
        self._max_reset = int(value)

    @property
    def max_ts_num(self):
        return self._max_ts_num

    @max_ts_num.setter
    def max_ts_num(self, value):
        self._max_ts_num = int(value)

    @property
    def max_thread_num(self):
        return self._max_thread_num

    @max_thread_num.setter
    def max_thread_num(self, value):
        self._max_thread_num = int(value)

    @property
    def auto_remove_ts(self):
        return self._auto_remove_ts

    @auto_remove_ts.setter
    def auto_remove_ts(self, value):
        self._auto_remove_ts = value != 0 and value != "0"