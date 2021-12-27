#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from graphics_audial import Graphic
from logic import test_logic

app = QApplication([])
first_window = Graphic()
logic = test_logic(parent = first_window, reverse_seq=True)

first_window.start_event.connect(logic.start_testing)
first_window.next_element_needed.connect(logic.emit_number)

logic.number_to_show_event.connect(first_window.play_element)

first_window.press_event.connect(logic.match_check)
logic.test_ended.connect(first_window.say_goodbye)

logic.play_sound_signal.connect(first_window.color_buttons)

app.exec_()

logic.print_results()


