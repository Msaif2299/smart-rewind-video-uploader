from PyQt5.QtWidgets import QLabel

LABEL_CHAR_LIMIT = 21

class DisplayFileLocLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("")
        self.setFixedWidth(150)
    
    def setText(self, text: str):
        display_text = "Not Selected"
        if text == "":
            self.setToolTip("")
        else:
            self.setToolTip(text)
        if len(text) > LABEL_CHAR_LIMIT:
            display_text = "..." + text[-LABEL_CHAR_LIMIT+3:]
        super().setText(display_text)
    