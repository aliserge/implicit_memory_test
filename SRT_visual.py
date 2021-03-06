#!/usr/bin/env python3
from logic.logcatcher import set_log_catcher
set_log_catcher()

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import PYQT_VERSION_STR
except ImportError:
    print("Can't import PyQt5 library")
    exit(-1)

print(f'PyQt: {PYQT_VERSION_STR}')

from ui.graphics_visual import Graphic
from logic.logic import Test_Logic

app = QApplication([])
first_window = Graphic()
logic = Test_Logic(parent=first_window)

first_window.start_event.connect(logic.start_testing)
first_window.next_element_needed.connect(logic.emit_number)

logic.number_to_show_event.connect(first_window.show_square)

first_window.press_event.connect(logic.match_check)
logic.test_ended.connect(first_window.say_goodbye)
logic.play_sound_signal.connect(first_window.play_sound)

app.exec_()

logic.print_results()
