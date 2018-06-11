#!/bin/bash
#
# Author:
#   Ricardo Santos <ricardos.geral at gmail.com>
#
# Description:
# A post-installation bash script for 2018-03-13-raspbian-stretch
# A raspbian post-install script for relier (Erosion Laboratory Test Software) server
# Usage: see README.md https://github.com/Ricardosgeral/relier/blob/master/README.md
#
# check if sudo is used
if [ "$(id -u)" != 0 ]; then
  echo 'Sorry, you need to run this script with sudo'
  exit 1
fi
clear
#
echo '------------------------------------------------------------------------'
echo '=> Raspbian post-install script for relier... pick a very hot cup of tea'
echo '------------------------------------------------------------------------'
echo '               '
#
echo '---------------------------'
echo '=> System update/upgrade   '
echo '---------------------------'
echo '=> Update repository information'
sudo apt-get update -qq
echo '=> Performe system upgrade'
sudo apt-get dist-upgrade -y
echo 'Done.'
#
echo  '---------------------------------------------------------------------------'
echo  '=> Folder to save the data values from sensors csv (comma separated values)'
echo  '---------------------------------------------------------------------------'
#
if [ -d "/srv/EROSTESTS/" ]; then
    echo 'Directory /srv/EROSTESTS/ already exists'
else
    sudo mkdir /srv/EROSTESTS
fi
#
if [ -d "/media/pi/" ]; then
    echo 'Directory /media/pi/ already exists'
else
    sudo mkdir /media/pi/
fi
#
# permissions
sudo chmod -R 777 /srv/EROSTESTS
sudo chown pi:pi /media/pi
sudo chmod -R 777 /media/pi
#
echo '------------------------------'
echo ' => Get repository from Gibhub'
echo ' -----------------------------'
#
if [ -d "/home/pi/relier" ]; then
    sudo rm -R /home/pi/relier
fi
git clone https://github.com/Ricardosgeral/relier.git /home/pi/relier
#these following two lines may be unnecessary
sudo chown -R pi: /home/pi/relier
sudo chmod 777 -R relier/
#
echo  '---------------------------'
echo  '=> Install system utilities'
echo  '---------------------------'
echo '=> Install system utilities'
#sudo apt-get install -y .....whatever you want e.g. latex
echo 'Done.'
#
echo  '------------------------------------------'
echo  '=> Install developer packages (python 3.5)'
echo  '------------------------------------------'
echo '=> Install developer packages'
#
sudo pip3 install --upgrade pip
sudo pip3 install pygsheets
sudo pip3 install --upgrade oauth2client
sudo pip3 install --upgrade pyasn1-modules # required for pysheets !!!
sudo pip3 install configparser
sudo pip3 install https://github.com/nithinmurali/pygsheets/archive/master.zip
sudo pip3 install adafruit-ads1x15
sudo pip3 install RPi.bme280
sudo pip3 install w1thermsensor
echo 'Done.'
#
echo '---------------------'
echo '=> Enable SSH and VNC'
echo '---------------------'
#
echo '>>> Enable SSH and VNC'
sudo raspi-config nonint do_ssh 0
sudo raspi-config nonint do_vnc 0
echo 'Done.'
#
echo  '--------------------------------------------------'
echo  '=> Configurations for serial, 1-Wire, I2C and UART'
echo  '--------------------------------------------------'
#
# enable 1-Wire GPIO on Raspberry Pi
echo '>>> Enable 1-Wire GPIO (w1)'
if grep -q 'dtoverlay=w1-gpio' /boot/config.txt; then
  echo 'Seems w1-gpio parameter already set, skip this step.'
else
  echo dtoverlay=w1-gpio >> /boot/config.txt
fi
#
# enable I2C on Raspberry Pi
echo '>>> Enable I2C'
sudo raspi-config nonint do_i2c 0
if grep -q 'dtparam=i2c_arm=on' /boot/config.txt; then
  echo 'i2c_arm already on'
else
  echo 'dtparam=i2c_arm=on' >> /boot/config.txt
fi
if grep -q 'dtparam=i2c1=on' /boot/config.txt; then
  echo 'i2c1 already on'
else
  echo 'dtparam=i2c1=on' >> /boot/config.txt
fi
echo 'dtparam=i2c_baudrate=400000' >> /boot/config.txt
#
# configure UART (Enable pins 14 and 15 to ttyAMA0 and Bluetooth to miniuart (which has limitations))
# start by disabling the serial console
echo '>>> Disable serial console'
sudo raspi-config nonint do_serial 1
sleep 2
echo '>>> Configure UART/Bluetooth'
if grep -q 'enable_uart=1' /boot/config.txt; then
  echo 'Seems Uart already enabled in 14/15 pins, skip this step.'
else
  echo enable_uart=1 >> /boot/config.txt
fi
if grep -q 'dtoverlay=pi3-disable-bt' /boot/config.txt; then
  echo 'Seems bluetooth on 14/15 already disabled, skip this step.'
else
  echo dtoverlay=pi3-disable-bt >> /boot/config.txt
fi
#
#Stop Bluetooth modem to use UART
sudo systemctl disable hciuart
echo 'Done.'
#
echo  '----------------------------------------------------------------'
echo  '=> Create systemd unit file for hotplugging (mount/unmount) usb'
echo  '----------------------------------------------------------------'
#
#Create a script to run at power up
sudo cp /home/pi/relier/bash/usb-mount.sh /usr/local/bin/usb-mount.sh
sudo sed -i 's/\r//' /usr/local/bin/usb-mount.sh
#
#Call the script by a system unit file
sudo cp /home/pi/relier/services/usb-mount@.service /etc/systemd/system/usb-mount@.service
#
#Add the two rules (file 99-local.rules) to start and stop system unit service on hotplug/unplug
sudo echo 'KERNEL== "sd[a-z][0-9]", SUBSYSTEMS=="usb", ACTION=="add", RUN+="/bin/systemctl start usb-mount@%k.service"' >> /etc/udev/rules.d/99-local.rules
sudo echo 'KERNEL=="sd[a-z][0-9]", SUBSYSTEMS=="usb", ACTION=="remove", RUN+="/bin/systemctl stop usb-mount@%k.service"'>> /etc/udev/rules.d/99-local.rules
#
sudo udevadm control -l debug           #allows debugging (tail –f /var/log/syslog, and plug/unplug a usb stick)
sudo udevadm control --reload-rules     #reloads rules
sudo systemctl daemon-reload            #reloads systemd
#
echo 'Done.'
#
echo '--------------------------------------------------------'
echo ' => Create systemd unit file to run at shutdown/reboot'
echo ' -------------------------------------------------------'
#
#Create a script to run at shutdown/reboot
sudo cp /home/pi/relier/services/rcshut.service /etc/systemd/system/rcshut.service
sudo systemctl enable rcshut --now
sudo systemctl start rcshut
sudo chmod +w /home/pi/relier/shutdown.py
echo 'Done.'
#
echo  '----------------------------------------------------------------'
echo  '=> Create systemd unit file to control shutdown/restart button'
echo  '----------------------------------------------------------------'
#
#Create a script to run at shutdown/reboot
#sudo apt install python3-gpiozero this should be not needed because is already in raspbian now
sudo cp /home/pi/relier/services/shutdown_button.service /etc/systemd/system/shutdown_button.service
sudo systemctl daemon-reload
sudo systemctl enable shutdown_button --now
sudo systemctl start shutdown_button
sudo chmod +w /home/pi/relier/shutdown_button.py
echo 'Done.'
#
echo  '---------------------------------------------------------'
echo  '=> Configurations of cron tab (files to run at startup)'
echo  '---------------------------------------------------------'
#
# First remove all cron's
crontab -r
#
CMD="/usr/bin/pigpiod"
JOB="@reboot $CMD"
TMPC="mycron1"
sudo grep "$CMD" -q <(crontab -l) || (crontab -l>"$TMPC"; echo "$JOB">>"$TMPC"; crontab "$TMPC")
echo 'Done.'
#
echo  '-----------------------------------------------------------------------------'
echo  '=> run main.py at start-up of raspberry pi (using a shell script in crontab)'
echo  '-----------------------------------------------------------------------------'
# make the launcher script an executable
sudo chmod 755 /home/pi/relier/bash/launcher.sh
echo 'Create a logs directory'
sudo mkdir /home/pi/relier/logs
sudo chmod 777 -R /home/pi/relier/logs
#
CMD="sh /home/pi/relier/bash/launcher.sh >/home/pi/relier/logs/cronlog 2>&1"
JOB="@reboot $CMD"
TMPC="mycron2"
sudo grep "$CMD" -q <(crontab -l) || (crontab -l>"$TMPC"; echo "$JOB">>"$TMPC"; crontab "$TMPC")
echo 'Done.'
#
echo  '----------------------------------------------------'
echo  '=> Install python3.6  (for Dash and pandas with python3.6)'
echo  '----------------------------------------------------'
#
#If one of the packages cannot be found, try a newer version number (e.g. libdb5.4-dev instead of libdb5.3-dev).
sudo apt-get -y install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
tar xf Python-3.6.5.tar.xz
./Python-3.6.5/configure
make
sudo make altinstall
sudo rm -r Python-3.6.5
sudo rm Python-3.6.5.tar.xz
sudo pip3.6 install --upgrade pip
sudo pip3.6 install numpy
sudo pip3.6 install pandas
sudo pip3.6 install pandas
sudo pip3.6 install configparser
sudo pip3.6 install dash==0.21.1  # The core dash backend
sudo pip3.6 install dash-renderer==0.13.0  # The dash front-end
sudo pip3.6 install dash-html-components==0.11.0  # HTML components
sudo pip3.6 install dash-core-components==0.23.0  # Supercharged components
sudo pip3.6 install plotly --upgrade  # Plotly graphing library used in examples
## some cleaning
#sudo apt-get -y --purge remove build-essential tk-dev
#sudo apt-get -y --purge remove libncurses5-dev libncursesw5-dev libreadline6-dev
## Adjust version numbers if necessary
#sudo apt-get -y --purge remove libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev
#sudo apt-get -y --purge remove libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
#sudo apt-get -y autoremove
#sudo apt-get -y clean
#
echo  '--------------------'
echo  '=> Final reboot'
echo  '--------------------'
#
if [ -f "/tmp/raspbian-post-install.sh" ]; then
sudo rm /tmp/raspbian-post-install.sh
fi
echo '>> Rebooting'
#
sudo reboot