#!/usr/bin/env python3
import sys
import platform

pythonStr = f"Python version: {sys.version}"
osStr = f"Operating system: {platform.system()}, {platform.release()} - {platform.version()}"

print("Graphic env test")
print(pythonStr)
print(osStr)

try:
    from PyQt5.QtWidgets import QApplication, QLabel
    from PyQt5.QtCore import PYQT_VERSION_STR, Qt
except ImportError:
    print("Can't import PyQt5 library ")
    exit(-1)

app = QApplication([])
pyQtStr = f"PyQt version: {PYQT_VERSION_STR}"
window = QLabel(f'<b>Graphic environment works correctly</b> <br>{pythonStr}<br>{osStr}<br>{pyQtStr}')
window.setMinimumSize(300, 300)
window.setAlignment(Qt.AlignCenter)
window.show()
app.exec_()

