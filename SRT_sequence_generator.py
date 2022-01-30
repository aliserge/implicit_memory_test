#!/usr/bin/env python3

from pickle import dump
from configparser import ConfigParser
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QGridLayout,
    QDoubleSpinBox,
    QSpinBox,
)
from logic.test_strategies import (
    Test_Strategy_Random,
    Test_Strategy_Learn,
    Test_Strategy_Kaufman,
)

seq_a_Kaufman = "1,2,1,4,3,2,4,1,3,4,2,3"
seq_b_Kaufman = "3,2,3,4,1,2,4,3,1,4,2,1"
config_file_name = "config.ini"
data_file_name = "sequence.pickle"


class Sequence_generator_window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        grid = QGridLayout()
        seq_a_label = QLabel("Sequence A:")
        seq_b_label = QLabel("Sequence B:")
        self.seq_a = QLineEdit()
        self.seq_a.setEnabled(False)
        self.seq_a.setText(seq_a_Kaufman)
        self.seq_a.setMinimumWidth(300)
        self.seq_b = QLineEdit()
        self.seq_b.setEnabled(False)
        self.seq_b.setText(seq_b_Kaufman)
        row = 0
        grid.addWidget(seq_a_label, row, 0)
        grid.addWidget(self.seq_a, row, 1)
        row += 1
        grid.addWidget(seq_b_label, row, 0)
        grid.addWidget(self.seq_b, row, 1)
        row += 1

        random_repeats_label = QLabel("Number of random repeats:")
        self.random_repeats = QSpinBox()
        self.random_repeats.setMinimum(1)
        self.random_repeats.setMaximum(10)
        self.random_repeats.setValue(4)
        grid.addWidget(random_repeats_label, row, 0)
        grid.addWidget(self.random_repeats, row, 1)
        row += 1

        learn_repeats_label = QLabel("Number of learn repeats circles:")
        self.learn_repeats = QSpinBox()
        self.learn_repeats.setMinimum(1)
        self.learn_repeats.setMaximum(10)
        self.learn_repeats.setValue(4)
        grid.addWidget(learn_repeats_label, row, 0)
        grid.addWidget(self.learn_repeats, row, 1)
        row += 1

        repeats_label = QLabel("Maximum test length:")
        self.test_repeats = QSpinBox()
        self.test_repeats.setMinimum(1)
        self.test_repeats.setMaximum(5000)
        self.test_repeats.setValue(600)
        self.test_repeats.setSingleStep(10)
        grid.addWidget(repeats_label, row, 0)
        grid.addWidget(self.test_repeats, row, 1)
        row += 1

        jump_probability_label = QLabel("Jump probability from A to B:")
        self.jump_probability = QDoubleSpinBox()
        self.jump_probability.setMinimum(0)
        self.jump_probability.setMaximum(1)
        self.jump_probability.setSingleStep(0.05)
        self.jump_probability.setValue(0.15)
        grid.addWidget(jump_probability_label, row, 0)
        grid.addWidget(self.jump_probability, row, 1)
        row += 1

        max_control_label = QLabel("Maximum stay in control sequence (B):")
        self.max_control = QSpinBox()
        self.test_repeats.setMinimum(6)
        self.max_control.setMaximum(24)
        self.max_control.setValue(8)
        grid.addWidget(max_control_label, row, 0)
        grid.addWidget(self.max_control, row, 1)
        row += 1

        generate_button = QPushButton("Generate sequence")
        generate_button.clicked.connect(self.generate)
        grid.addWidget(generate_button, row, 0, 1, 2)

        self.setLayout(grid)
        self.show()

    def generate(self):
        seq_a = self.seq_a.text().split(",")
        seq_b = self.seq_b.text().split(",")

        strategy_random = Test_Strategy_Random(self.random_repeats.value())
        seq_random = [el for el in strategy_random]
        strategy_learn = Test_Strategy_Learn(seq_a, self.learn_repeats.value())
        seq_learn = [el for el in strategy_learn]
        strategy_kaufman = Test_Strategy_Kaufman(
            seq_a,
            seq_b,
            self.test_repeats.value(),
            self.jump_probability.value(),
            self.max_control.value(),
        )
        seq_test = [el for el in strategy_kaufman]

        #seq = seq_random + seq_learn + seq_test
        #for el in seq:
        #    print(el)
        with open(data_file_name, "wb") as data_file:
            dump(seq_random, data_file)
            dump(seq_learn, data_file)
            dump(seq_test, data_file)

        config = ConfigParser()
        config["Sequences"] = {"seq_a": self.seq_a.text(), "seq_b": self.seq_b.text()}

        config["Settings"] = {
            "random_repeats": len(seq_random),
            "learn_repeats": len(seq_learn),
            "test_repeats": len(seq_test),
            "jump_probability": self.jump_probability.value(),
            "max_control": self.max_control.value(),
        }

        config["Datafile"] = {"data_file_name": data_file_name}

        with open(config_file_name, "w") as config_file:
            config.write(config_file)

        app.quit()


app = QApplication([])
first_window = Sequence_generator_window()
app.exec_()
