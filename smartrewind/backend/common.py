from typing import Optional
import time

from smartrewind.progresstracker.statemachine import ProgressStateMachine

def emit(progress_state_machine:Optional[ProgressStateMachine], value: int, message: str):
    if progress_state_machine is not None:
        progress_state_machine.forward_progress_signal.emit(value, message)
        #test
        time.sleep(1)