#!/bin/bash
# launcher.sh
# navigate to home directory, then to this directory, then execute python3scrip$
Sleep 13            # required to allow complete boot of raspbian
cd /home/pi/LerAS
python3 main.py
