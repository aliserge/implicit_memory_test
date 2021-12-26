#!/usr/bin/python3

import os

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QGridLayout, QVBoxLayout, QMessageBox, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QEventLoop, QTimer
from PyQt5.QtGui import QPalette

from PyQt5.QtMultimedia import QSound
from user_input import User_input

sound_dir = 'sounds'

class Graphic(QWidget):
    next_element_needed = pyqtSignal()
    press_event = pyqtSignal(str)
    goodbye_event = pyqtSignal()
    start_event = pyqtSignal(str, str)
    sleep_time = 500
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.sounds = [QSound(os.path.join(sound_dir, "one.wav")),
            QSound(os.path.join(sound_dir, "two.wav")),
            QSound(os.path.join(sound_dir, "three.wav")),
            QSound(os.path.join(sound_dir, "four.wav")) ]
        self.red = QPalette()
        self.red.setColor(QPalette.Button, Qt.red)
        self.green = QPalette()
        self.green.setColor(QPalette.Button, Qt.green)
        self.neutral = QPalette()
        
        
    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.user_name_date = User_input()
        self.user_name_date.start_btn.clicked.connect(self.btn_start_clicked)
        

        self.layout.addWidget(self.user_name_date, 0, 0, 1, 4, alignment = Qt.AlignCenter)
        self.btns = [ QPushButton(str(i+1)) for i in range(4) ]
        
        for i,btn in enumerate(self.btns):
            self.layout.addWidget(btn, 1, i)
            btn.setEnabled(False)
            btn.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
            font = btn.font()
            font.setPointSize(32)
            btn.setFont(font)
            #btn.setAutoFillBackground(True)
            
        self.btns[0].clicked.connect(self.btn_1)
        self.btns[1].clicked.connect(self.btn_2)
        self.btns[2].clicked.connect(self.btn_3)
        self.btns[3].clicked.connect(self.btn_4)
        
        self.showMaximized()

    def btn_start_clicked(self):
        self.user_name_date.hide()
        QMessageBox.warning(self, 'The rules', """Press 1, 2, 3, 4 
buttons on the screen
according to numbers you hear 
as accurate and rapid as possible""")
        
        for btn in self.btns:
            btn.setEnabled(True)
        
        self.start_event.emit(self.user_name_date.name_line.text(), self.user_name_date.date_birth_line.text())
        self.next_element_needed.emit()
    
    def btn_1(self):
        self.btn_pressed(1)

    def btn_2(self):
        self.btn_pressed(2)
        
    def btn_3(self):
        self.btn_pressed(3)
        
    def btn_4(self):
        self.btn_pressed(4)
    
    def btn_pressed(self, btn_number):
        
        self.btn_pressed_number = btn_number-1
        
        self.press_event.emit(str(btn_number))
        for btn in self.btns:
            btn.setEnabled(False)
        
        loop = QEventLoop()
        QTimer.singleShot(self.sleep_time, loop.quit)
        loop.exec_()
        
        for btn in self.btns:
            btn.setEnabled(True)
            btn.setPalette(self.neutral)
            
        self.next_element_needed.emit()
        
    def say_goodbye(self):
        QMessageBox.warning(self, 'The end', """The testing is completed. Thank you!""")
        self.goodbye_event.emit()
        self.close()
        
    def play_element(self, n):
        print("Play element ",n)
        n = int(n)-1
        self.sounds[n].play()
        
    def color_buttons(self, is_correct):
        if is_correct == "True":
            palette = self.green
        else:
            palette = self.red
        self.btns[self.btn_pressed_number].setPalette(palette)
        
        
        



