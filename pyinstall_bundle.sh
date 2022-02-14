#!/bin/bash

#pyi-makespec SRT_sequence_generator.py
#pyi-makespec SRT_audial.py
#pyi-makespec SRT_visual.py

pyinstaller -y SRT_sequence_generator.py
pyinstaller -y SRT_audial.py 
pyinstaller -y SRT_visual.py 
pyinstaller -y test_graphics.py 

cp config.ini dist
cp sequence.pickle dist
