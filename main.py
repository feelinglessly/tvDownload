import sys
import platform
from config import init_config, set_verify, get_config
from platforms.haitu import HaiTuScheduler
from platforms.huaren import HuaRenScheduler
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QLabel, QVBoxLayout, QWidget,
    QHBoxLayout, QLineEdit, QButtonGroup, QRadioButton
)

from platforms2.yuny import YunYScheduler
from qt.app import MainWindow
from stores.data import VideoData

def new(data: VideoData):
    print('new data', data.uuid)
    set_verify(data.verify == "是")
    config = get_config()
    if data.platform == "华人":
        spider = HuaRenScheduler(
            data.uuid,
            data.host_line,
            data.url_line,
            data.file_dir,
            data.auto_next,
            config.app.max_reset,
            config.app.max_ts_num,
            max_thread_num=config.app.max_thread_num,
            auto_remove_ts=config.app.auto_remove_ts,
        )
    elif data.platform == "云影":
        spider = YunYScheduler(
            data.uuid,
            data.host_line,
            data.url_line,
            data.file_dir,
            data.auto_next,
            config.app.max_reset,
            config.app.max_ts_num,
            max_thread_num=config.app.max_thread_num,
            auto_remove_ts=config.app.auto_remove_ts,
        )
    else:
        spider = HaiTuScheduler(
            data.uuid,
            data.host_line,
            data.url_line,
            data.file_dir,
            data.auto_next,
            config.app.max_reset,
            config.app.max_ts_num,
            max_thread_num=config.app.max_thread_num,
            auto_remove_ts=config.app.auto_remove_ts,
        )
    return spider


if __name__ == '__main__':
    system = platform.system()
    if system == 'Windows':
        f = "config.yaml"
    else:
        f = "mac_config.yaml"
    init_config(f)

    app = QApplication(sys.argv)
    window = MainWindow("视频下载程序", func=new)  # 创建我们自定义的主窗口实例
    window.show()
    sys.exit(app.exec())
