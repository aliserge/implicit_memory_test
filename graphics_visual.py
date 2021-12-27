#!/usr/bin/python3

import os

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QGridLayout, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QEventLoop, QTimer
from PyQt5.QtMultimedia import QSound
from user_input import User_input

sound_dir = 'sounds'

class Angle_square(QWidget):
    size = 300
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.initUI()
    def initUI(self):
        self.setFixedSize(self.size, self.size)
        self.red = QPalette()
        self.red.setColor(QPalette.Window, Qt.red)
        self.white = QPalette()
        self.white.setColor(QPalette.Window, Qt.white)

    def become_red(self):
        self.setPalette(self.red)

    def become_white(self):
        self.setPalette(self.white)

      

class Graphic(QWidget):
    next_element_needed = pyqtSignal()
    press_event = pyqtSignal(str)
    goodbye_event = pyqtSignal()
    start_event = pyqtSignal(str, str)
    keys_to_numbers = {"1":"1","3":"2","7":"3","9":"4"}
    sleep_time = 500
    
    def __init__(self):
        super().__init__()
        self.squares = {1: Angle_square(), 2: Angle_square(), 3: Angle_square(), 4: Angle_square()}
        self.wait_for_key = False
        self.correct_answer_sound = QSound(os.path.join(sound_dir, "positive-notification.wav"))
        self.wrong_answer_sound = QSound(os.path.join(sound_dir, "wrong-answer.wav"))
        
        self.initUI()
    
    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.addWidget(self.squares[1], 2, 0)
        self.grid.addWidget(self.squares[3], 0, 0)
        self.grid.addWidget(self.squares[2], 2, 2)
        self.grid.addWidget(self.squares[4], 0, 2)
        self.user_name_date = User_input()
        self.user_name_date.start_btn.clicked.connect(self.btn_start_clicked)
        self.grid.addWidget(self.user_name_date, 1, 1, Qt.AlignCenter)
        
        self.showMaximized()

    def btn_start_clicked(self):
        self.user_name_date.hide()
        QMessageBox.warning(self, 'The rules', """Press 1, 3, 7, 9 
using the number part of the keyboard 
according to appearing red squares 
in the corners of the screen 
as accurate and rapid as possible""")
        for square in self.squares.values():
            square.become_white()
        self.start_event.emit(*self.user_name_date.user_data())
        self.next_element_needed.emit()
    
    def show_square(self, square_number):
        square_number = int(square_number)
        print("Recieved square to show:", square_number)
        
        self.squares[square_number].become_red()
        self.wait_for_key = True
        
    def keyPressEvent(self, e):
        if not self.wait_for_key:
            super().keyPressEvent(e)
            return
        self.wait_for_key = False
        
        key = e.text()
        print("Key_catched: ", key)
        
        if key in self.keys_to_numbers.keys():
            key = self.keys_to_numbers[key]
        
        self.press_event.emit(key)
        
        for square in self.squares.values():
            square.become_white()
        
        loop = QEventLoop()
        QTimer.singleShot(self.sleep_time, loop.quit)
        loop.exec_()
        
        self.next_element_needed.emit()
    
    def say_goodbye(self):
        QMessageBox.warning(self, 'The end', """The testing is completed. Thank you!""")
        self.goodbye_event.emit()
        self.close()
        
    def play_sound(self, is_correct):
        if is_correct == 'True':
            self.correct_answer_sound.play()
        else:
            self.wrong_answer_sound.play()



