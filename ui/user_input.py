from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QSizePolicy, QDateEdit

class User_input(QWidget):
    def __init__(self):
        super().__init__()

        central = QVBoxLayout()
        name_lbl = QLabel('Name:')
        name_lbl.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        # move
        self.name_line = QLineEdit()
        self.name_line.textChanged.connect(self.check_name_correctness)
        # move
        date_birth_lbl = QLabel('Date of birth:')
        self.date_birth_line = QDateEdit()
        self.date_birth_line.setCalendarPopup(True)

        self.start_btn = QPushButton('Start')
        #self.start_btn.clicked.connect(self.start_pressed)
        self.start_btn.setEnabled(False)

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
    
    def check_name_correctness(self):
        self.start_btn.setEnabled(self.name_line.text() != '')
    
    def start_pressed(self):
        self.start_btn.setEnabled(False)
        
    def user_data(self):
        return self.name_line.text(), self.date_birth_line.date().toString('yyyy-MM-dd')
