#!/bin/bash
# launcher.sh
# navigate to home directory, then to this directory, then execute python3 scrip$
sleep 8            # required to allow complete boot of Raspbian
cd /home/pi/relier
python3 main.py
