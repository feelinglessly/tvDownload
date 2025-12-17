from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QLabel, QVBoxLayout, QWidget,
    QHBoxLayout, QLineEdit, QRadioButton, QButtonGroup, QFileDialog, QTextEdit
)

from PySide6.QtGui import QCursor, QPixmap, Qt

from qt.base import WidgetEditValueMixIn, WidgetEditValueSetMixIn


def on(*args, **kwargs):
    return None


class Label(QLabel):
    def __init__(self, label, tips, *args, **kwargs):
        super().__init__(label, *args, **kwargs)
        if tips is not None:
            self.setToolTip(tips)


class PushButton(QPushButton):
    style = ""
    _style = ""
    size = "small"
    map = {"small": 2, "large": 10}
    def __init__(self, label, onclick=on, style="common", size="small", *args, **kwargs):
        super().__init__(label)
        self.size = size
        self._style = style
        self.change_style(style)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # 设置点击回调
        self.onclick(onclick)

    def onclick(self, onclick, *args, **kwargs):
        self.clicked.connect(onclick)

    def change_onclick(self, onclick, f):
        self.onclick(f)

    def change_style(self, style):
        self.style = style
        self._set_style()

    def _set_style(self):
        if self.style == "success":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;  /* 绿色背景 */
                    color: white;               /* 白色文字 */
                    padding: """+str(self.map[self.size])+"""px;
                }
            """)
            # border-radius: 1px;
        elif self.style == "warning":
            self.setStyleSheet("""
            QPushButton {
                background-color: #FF7F00;
                color: black;
                padding: """+str(self.map[self.size])+"""px;
                }
            """)
        elif self.style == "info":
            self.setStyleSheet("""
                        QPushButton {
                            background-color: #D3D3D3;
                            color: black;
                            padding: """ + str(self.map[self.size]) + """px;
                            }
                        """)
        else:
            pass

    def enable(self):
        self.setEnabled(True)
        self.change_style(self._style)

    def unable(self):
        self.setEnabled(False)
        self.change_style("info")


class LineEdit(QLineEdit, WidgetEditValueMixIn):
    placeholder = ""
    def __init__(self, placeholder, onchange=on, *args, **kwargs):
        super().__init__()
        self.placeholder = placeholder
        self.set_placeholder(placeholder)
        # self.onchange(onchange)

    def set_placeholder(self, placeholder=None):
        """
        :param placeholder: 为None时将还原
        :return:
        """
        self.setPlaceholderText(placeholder if placeholder is not None else self.placeholder)

    def set_text(self, text):
        self.setText(text)

    def onchange(self, f):
        """
        :param f: 内容变化时调用
        :return:
        """
        self.textChanged(f)
    def value(self):
        return self.text()


class RadioButtonGroup(QButtonGroup, WidgetEditValueMixIn):
    radios = None
    def __init__(self, parent, *labels, clicked=None, exclusive=True):
        """
        :param parent: 父组件
        :param labels: 选项值
        :param clicked: 选择值
        :param exclusive: 是否互斥
        """
        super().__init__(parent)
        self.radios = []
        for label in labels:
            radio = QRadioButton(label)
            radio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            if label == clicked and clicked is not None:
                radio.setChecked(True)
            self.add_radio(radio)
        self.setExclusive(exclusive)

    def add_radio(self, radio):
        self.addButton(radio)
        self.radios.append(radio)

    def get_radios(self):
        return self.radios

    def value(self):
        for radio in self.radios:
            if radio.isChecked():
                return radio.text()
        return None


class FileSelector(QFileDialog, WidgetEditValueMixIn):
    def __init__(self, title=""):
        super().__init__()
        self.setFileMode(QFileDialog.FileMode.Directory)  # 只能选择文件夹
        self.setOption(QFileDialog.Option.ShowDirsOnly, True)
        self.setWindowTitle(title)

    def value(self):
        return self.selectedFiles()


class TextEdit(QTextEdit, WidgetEditValueMixIn, WidgetEditValueSetMixIn):
    def __init__(self, readonly=False):
        super().__init__()
        self.setReadOnly(readonly)

    def value(self):
        return self.toPlainText()

    def set_text(self, text):
        self.setText(text)

    def set_markdown(self, content):
        self.setMarkdown(content)
