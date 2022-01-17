#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QGridLayout, QVBoxLayout, QDoubleSpinBox, QSpinBox
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QEventLoop, QTimer
#from test_strategy import test_strategy_Kaufman

class Sequence_generator_window(QWidget):
    next_element_needed = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        #self.strategy = test_strategy_Kaufman()
        self.loadDefaults()
    
    def initUI(self):
        grid = QGridLayout()
        seq_a_label = QLabel("Sequence A:")
        seq_b_label = QLabel("Sequence B:")
        self.seq_a = QLineEdit()
        self.seq_a.setEnabled(False)
        self.seq_b = QLineEdit()
        self.seq_b.setEnabled(False)
        grid.addWidget(seq_a_label,0,0)
        grid.addWidget(self.seq_a,0,1)
        grid.addWidget(seq_b_label,1,0)
        grid.addWidget(self.seq_b,1,1)
        
        jump_probability_label = QLabel("Jump probability from A to B:")
        self.jump_probability = QDoubleSpinBox()
        self.jump_probability.setMaximum(1)
        self.jump_probability.setSingleStep(0.05)
        self.jump_probability.setValue(0.15)
        grid.addWidget(jump_probability_label,2,0)
        grid.addWidget(self.jump_probability,2,1)
        
        repeats_label = QLabel("Maximum test length:")
        self.repeats = QSpinBox()
        self.repeats.setMaximum(5000)
        self.repeats.setValue(600)
        self.repeats.setSingleStep(10)
        grid.addWidget(repeats_label,3,0)
        grid.addWidget(self.repeats,3,1)
        
        generate_button = QPushButton("Generate sequence")
        generate_button.clicked.connect(self.generate)
        grid.addWidget(generate_button,4,0,1,2)
        
        self.setLayout(grid)
        self.show()

    def loadDefaults(self):
        pass
        
    def generate(self):
        pass

app = QApplication([])
first_window = Sequence_generator_window()
app.exec_()


