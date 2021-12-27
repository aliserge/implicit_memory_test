#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from graphics_visual import Graphic
from logic import test_logic

app = QApplication([])
first_window = Graphic()
logic = test_logic(parent = first_window)

first_window.start_event.connect(logic.start_testing)
first_window.next_element_needed.connect(logic.emit_number)

logic.number_to_show_event.connect(first_window.show_square)

first_window.press_event.connect(logic.match_check)
logic.test_ended.connect(first_window.say_goodbye)
logic.play_sound_signal.connect(first_window.play_sound)

app.exec_()

logic.print_results()


