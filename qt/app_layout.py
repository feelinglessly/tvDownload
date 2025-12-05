from qt.base import WidgetEditValueMixIn
from qt.layout import HBoxLayout
from qt.widgets import RadioButtonGroup, LineEdit, PushButton, FileSelector, Label
from PySide6.QtWidgets import (
    QLabel
)
from PySide6.QtCore import Qt


class HRadiosLayout(HBoxLayout, WidgetEditValueMixIn):
    """
    横向的单选按钮
    """
    group = None
    def __init__(self, label=None, *radio_labels, clicked=None, tips=None):
        """
        :param label: 左侧显示
        :param radio_labels: 选项显示
        :param clicked: 选项
        """
        super().__init__()
        bg = RadioButtonGroup(self,*radio_labels, clicked=clicked)
        if label is not None:
            self.set_widgets(Label(label, tips))
        self.set_widgets(*bg.get_radios())
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.group = bg

    def value(self):
        return self.group.value()



class LineEditLayout(HBoxLayout, WidgetEditValueMixIn):
    input_line = None
    def __init__(self, label, placeholder):
        super().__init__()
        input_label = QLabel(label)
        input_line = LineEdit(placeholder)

        self.addWidget(input_label)
        self.addWidget(input_line)
        self.input_line = input_line

    def set_line_text(self, text):
        self.input_line.setText(text)

    def value(self):
        return self.input_line.value()


class FileSelectLayout(HBoxLayout, WidgetEditValueMixIn):
    select_title = "选择文件夹"
    file_dialog = None
    def __init__(self, label, placeholder, select_title=None):
        super().__init__()

        if select_title is not None:
            self.select_title = select_title
        file_dialog = FileSelector(self.select_title)
        self.file_dialog = file_dialog

        btn_browse = PushButton("浏览...", self.open_file_dialog)
        input_label = QLabel(label)
        input_field = LineEdit(placeholder)
        self.input_field = input_field

        self.addWidget(input_label)
        self.addWidget(input_field)
        self.addWidget(btn_browse)

    def open_file_dialog(self):

        if self.file_dialog.exec():
            selected_files = self.file_dialog.selectedFiles()
            if selected_files:
                folder_path = selected_files[0]
                print("选择的文件夹:", folder_path)
                self.input_field.setText(folder_path)  # 显示在输入框中

    def value(self):
        return self.input_field.value()

    def set_line_text(self, text):
        self.input_field.setText(text)