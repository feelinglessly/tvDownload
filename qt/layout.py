from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QLabel, QVBoxLayout, QWidget,
    QHBoxLayout, QLineEdit
)

# 横着一排
class HBoxLayout(QHBoxLayout):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_widgets(self, *widgets):
        for widget in widgets:
            self.addWidget(widget)
    def set_right_widgets(self, *widgets):
        self.addStretch()
        for widget in widgets:
            self.addWidget(widget)
    def set_layouts(self, *layouts):
        for layout in layouts:
            self.addLayout(layout)

    def set_right_layouts(self, *layouts):
        self.addStretch()
        for layout in layouts:
            self.addLayout(layout)

# 竖着一排
class VBoxLayout(QVBoxLayout):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def set_widgets(self, *widgets):
        for widget in widgets:
            self.addWidget(widget)
    def set_layouts(self, *layouts):
        for layout in layouts:
            self.addLayout(layout)

    def set_right_layout(self, *layout):
        self.addStretch()
        for widget in layout:
            self.setWidget(widget)

