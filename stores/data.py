
VideoDataStatusInit = "init"
VideoDataStatusPadding = "padding"
VideoDataStatusRunning = "running"
VideoDataStatusStop = "stop"
VideoDataStatusDone = "done"
VideoDataStatusError = "error"


class VideoData(object):
    uuid = ""
    platform = ""
    verify = ""
    auto_next = 0
    url_line = ""
    host_line = ""
    file_dir = ""
    pop = 0
    status = VideoDataStatusPadding
    error = ""
    nid = 0

    def __init__(self, uuid, platform, verify, auto_next, url_line, host_line, file_dir):
        self.uuid = uuid
        self.platform = platform
        self.verify = verify
        self.auto_next = 1 if auto_next == "是" else 0
        self.url_line = url_line
        self.host_line = host_line
        self.file_dir = file_dir
        self.status = VideoDataStatusInit

        self.nid = 0

    def done(self):
        if self.status == VideoDataStatusRunning:
            self.status = VideoDataStatusDone

    def stop(self):
        if self.status not in [VideoDataStatusDone, VideoDataStatusError]:
            self.status = VideoDataStatusStop

    def set_status(self, status):
        if status in [VideoDataStatusPadding, VideoDataStatusStop, VideoDataStatusRunning, VideoDataStatusDone, VideoDataStatusError]:
            self.status = status
        return

    def set_padding(self):
        if self.is_can_reset():
            self.status = VideoDataStatusPadding

    def set_running(self):
        if self.status in [VideoDataStatusRunning, VideoDataStatusStop, VideoDataStatusError, VideoDataStatusPadding]:
            self.status = VideoDataStatusRunning

    def set_error(self, error):
        self.error = error

    def is_padding(self):
        if self.status == VideoDataStatusPadding:
            return True
        return False

    def is_can_reset(self):
        if self.status in [VideoDataStatusStop, VideoDataStatusError, VideoDataStatusInit]:
            return True
        return False

    def set_nid(self, nid):
        self.nid = nid