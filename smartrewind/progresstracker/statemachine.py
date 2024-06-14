from PyQt5.QtCore import pyqtSignal, QObject

class ProgressStateMachine(QObject):
    forward_progress_signal = pyqtSignal(int,str)
    def __init__(self) -> None:
        super().__init__()
        self.current_progress = 0
        self.action_function = None
        self.forward_progress_signal[int,str].connect(self.forward)

    def set_action_func(self, func):
        self.action_function = func
    
    def forward(self, new_progress, message):
        if new_progress > self.current_progress:
            self.action_function(new_progress, message)
            self.current_progress = new_progress

