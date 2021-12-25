from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

class User_input(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        central = QVBoxLayout()
        name_lbl = QLabel('Name:')
        name_lbl.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        # move
        self.name_line = QLineEdit()
        # move
        date_birth_lbl = QLabel('Date of birth:')
        self.date_birth_line = QLineEdit()
        
        self.start_btn = QPushButton('Start')
        
        central.addStretch()
        central.addWidget(name_lbl)
        central.addWidget(self.name_line)
        self.name_line.setMaximumWidth(200)
        central.addWidget(date_birth_lbl)
        central.addWidget(self.date_birth_line)
        self.date_birth_line.setMaximumWidth(200)
        central.addWidget(self.start_btn)
        self.start_btn.setMaximumWidth(200)
        central.addStretch()
        self.setLayout(central)
