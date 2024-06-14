from PyQt5.QtWidgets import QLabel, QStyle
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

class UserActionStatusLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.tick_icon = self.style().standardIcon(QStyle.SP_DialogApplyButton)
        self.warning_icon = self.style().standardIcon(QStyle.SP_MessageBoxWarning)
        self.icon_size = QSize(16, 16)
        self.set_icon(self.warning_icon)

    def set_icon(self, icon:QIcon):
        self.setPixmap(icon.pixmap(self.icon_size))

    def set_positive_state(self):
        self.set_icon(self.tick_icon)

    def set_negative_state(self):
        self.set_icon(self.warning_icon)