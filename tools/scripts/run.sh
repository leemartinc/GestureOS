#!/bin/bash

clear
cd ~/Desktop/src/
mkfifo statusChange
python3 motionDetect.py &
python3 zoomDisplay.py 0.25 0.8
