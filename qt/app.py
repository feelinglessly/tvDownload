import sys
import threading

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QLabel, QVBoxLayout, QWidget,
    QHBoxLayout, QLineEdit, QButtonGroup, QRadioButton, QMessageBox
)

from PySide6.QtCore import Qt

from application.ctrl import Ctrl
from config import init_config, get_config
from qt.app_layout import HRadiosLayout, LineEditLayout, FileSelectLayout
from qt.layout import HBoxLayout
from qt.sync import SyncTextEdit
from qt.widgets import PushButton, FileSelector, TextEdit
from statics.api import get_file_path
from stores.data import VideoData
from stores.stores import get_store


# 将功能封装到一个类中，这是更结构化的方式
class MainWindow(QWidget):
    title = ""
    size = (100, 100, 400, 200)
    platform = None
    verify = None
    auto_next = None
    url_line = None # 应该只能有一个
    host_line = None
    file = None
    download_button = None
    add_button = None
    clear_button = None
    start_button = None
    stop_button = None
    callback = None
    spider = None
    ctrl = None
    works = None

    def __init__(self, title, size=(600, 600, 1600, 800), func=None, *args, **kwargs):
        super().__init__()  # 初始化父类
        self._text = None
        self.title = title
        self.size = size
        self.func = func
        self.init_ui()
        self.works = []
        self.ctrl = Ctrl(func=self.func)
        self.ctrl.start()

    def init_ui(self):
        conf = get_config()

        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(get_file_path("title.ico")))
        self.setGeometry(*self.size)
        self.add_button = PushButton(conf.app.add_button_text, self.on_add_clicked, "success", "large")
        self.clear_button = PushButton(conf.app.clear_button_text, self.on_clear_clicked, "warning", "large")
        self.start_button = PushButton(conf.app.start_button_text, self.on_start_clicked, "success", "large")
        self.stop_button = PushButton(conf.app.stop_button_text, self.on_stop_clicked, "warning", "large")

        platform = HRadiosLayout(
            conf.app.platform_label,
            *conf.app.platform_radios,
            clicked=conf.app.platform_clicked,
            tips=conf.app.platform_tips
        )

        verify = HRadiosLayout(
            conf.app.verify_label,
            *conf.app.verify_radios,
            clicked=conf.app.verify_clicked,
            tips=conf.app.verify_tips
        )
        auto_next = HRadiosLayout(
            conf.app.auto_next_label,
            *conf.app.auto_next_radios,
            clicked=conf.app.auto_next_clicked,
            tips=conf.app.auto_next_tips
        )

        h1 = HBoxLayout()
        h1.set_layouts(platform, verify, auto_next)

        url_line = LineEditLayout(conf.app.url_line_label, conf.app.url_line_placeholder)
        host_line = LineEditLayout(conf.app.host_line_label, conf.app.host_line_placeholder)
        file = FileSelectLayout(conf.app.file_label, conf.app.file_placeholder)
        # 设置布局
        layout = QVBoxLayout(self)
        layout.addLayout(h1)
        layout.addLayout(url_line)
        # layout.addLayout(host_line)
        layout.addLayout(file)

        _text = SyncTextEdit(True)

        # 按钮
        button_layout = HBoxLayout()
        button_layout.set_widgets(self.add_button)
        button_layout.set_widgets(self.clear_button)
        button_layout.set_right_widgets(self.start_button, self.stop_button)
        # layout.addWidget(self.add_button) # 添加按钮
        # layout.addWidget(self.start_button) # 添加按钮
        # layout.addWidget(self.stop_button) # 添加按钮
        layout.addLayout(button_layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(_text)

        self.platform = platform
        self.verify = verify
        self.auto_next = auto_next
        self.url_line = url_line
        self.host_line = host_line
        self.file = file
        self._text = _text

        self.text()

    def text(self):
        self.url_line.set_line_text("https://www.yuny.tv/videoPlayer/591212?detailId=35819")
        # self.host_line.set_line_text("https://www.ece8.com/")
        self.file.set_line_text(r"E:\project\watch\videos\dxjz")
        self._text.format_text([])

    def on_start_clicked(self):
        get_store().reset()
        self.ctrl.reset()
        self.start_button.unable()
        self.add_button.unable()
        self.clear_button.unable()
        self.stop_button.enable()

    def on_stop_clicked(self):
        get_store().stop()
        self.ctrl.stop()
        self.start_button.enable()
        self.add_button.enable()
        self.clear_button.enable()
        self.stop_button.unable()

    def on_add_clicked(self):
        data = VideoData(
            uuid=self.url_line.value(),
            platform=self.platform.value(),
            verify=self.verify.value(),
            auto_next=self.auto_next.value(),
            url_line=self.url_line.value(),
            host_line=self.host_line.value(),
            file_dir=self.file.value(),
        )
        store = get_store()
        store.push(data)

    def on_clear_clicked(self):
        get_store().clear()

    def close(self):
        print("xxx close")
        if self.spider is not None:
            self.spider.stop()
        # if self.thread.is_alive():
        #     self.thread.join()
        self.ctrl.close()

    def closeEvent(self, event):
        """处理窗口关闭事件"""
        reply = QMessageBox.question(
            self, "确认退出",
            "确定要退出程序吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.close()  # 准备退出
            event.accept()  # 接受关闭
        else:
            event.ignore()  # 忽略关闭


# 应用的主入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("视频下载程序")  # 创建我们自定义的主窗口实例
    window.show()
    app.exec()
    sys.exit()