# *erosLab* 
# Laboratory Erosion Test Software 
Open design of a monitoring acquisition system of a laboratory erosion test apparatus, using raspberry pi3 B as server, and python3 code. 

## Author
##### Ricardo Correia dos Santos
<ricardos.geral?@gmail.com>, <ricardos?@lnec.pt>    #remove '?' for real emails

The author developed this software at Laboratório Nacional de Engenharia Civil (LNEC),  in Lisbon, Portugal <www.lnec.pt/en/>

## Usage
These instructions should be carried out after a fresh installation of raspbian (tested with [2018-04-18-raspian-stretch](http://downloads.raspberrypi.org/raspbian/images/raspbian-2018-04-19/)). 

#### NOTE: If no monitor is available (headless raspberry pi 3), first you have to do these 4 steps.
1. Create an empty file (in windows use notepad | in Linux terminal use command *touch* | in Mac use TextEdit).
2. Save the file with name: ssh (ssh.txt should also work).
3. Copy or move the ssh file into the root of the sd card.
4. Put the SD card in RPi3B and power it on.

#### Connect to raspberry pi directly (if monitor is available) or via SSH (for example with putty). In this last option, you need to know the IP of the raspberry pi!

It is recommended to change the password of user pi, since SSH is enabled!

    $ passwd 
current password: *raspberry*

#### Next, in a terminal, run the following sequential commands:
    $ cd /tmp && wget https://raw.githubusercontent.com/Ricardosgeral/erosLab/master/bash/raspbian-post-install.sh
    $ sudo chmod +x raspbian-post-install.sh
    $ sed -i 's/\r//' raspbian-post-install.sh
    $ sudo ./raspbian-post-install.sh

#### Next, you need to create your own JSON file with the google credentials
To obtain it, see https://pygsheets.readthedocs.io/en/latest/authorizing.html#signed-credentials

    $ sudo nano /home/pi/erosLab/service_creds.json

Delete all content of the file and past your own credentials. Ctrl+X, yes and Enter to save file.

    $ sudo reboot

#### After reboot the server should be running properly (if hardware is also set correctly)!