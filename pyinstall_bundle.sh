#!/bin/bash
pyinstaller -y --onefile SRT_audial.py
pyinstaller -y --onefile SRT_visual.py
cp config.ini dist
