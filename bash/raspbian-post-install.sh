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

echo '-------------------------------------------------------------------------'
echo '=> Raspbian post-install script for relier... pick a very hot cup of tea'
echo '-------------------------------------------------------------------------'

# -----------------------------------------------------------------------------
# => System update/upgrade
# -----------------------------------------------------------------------------
echo '=> Update repository information'
sudo apt-get update -qq
echo '=> Performe system upgrade'
sudo apt-get dist-upgrade -y
echo 'Done.'

# -----------------------------------------------------------------------------
# => Folder to save the data values from sensors csv (comma separated values)
# -----------------------------------------------------------------------------

if [ -d "/srv/EROSTESTS/" ]; then
    echo 'Directory /srv/EROSTESTS/ already exists'
else
    sudo mkdir /srv/EROSTESTS
fi

if [ -d "/media/pi/" ]; then
    echo 'Directory /media/pi/ already exists'
else
    sudo mkdir /media/pi/
fi

# permissions
sudo chmod -R 777 /srv/EROSTESTS
sudo chown pi:pi /media/pi
sudo chmod -R 777 /media/pi

# -----------------------------------------------------------------------------
# => Get files from gibhub
# -----------------------------------------------------------------------------

if [ -d "/home/pi/relier" ]; then
    sudo rm -R /home/pi/relier
fi
git clone https://github.com/Ricardosgeral/relier.git /home/pi/relier
#these following two lines may be unnecessary
sudo chown -R pi: /home/pi/relier
sudo chmod 777 -R relier/

# ----------------------------------------------------------------------------
# => Install system utilities
# ----------------------------------------------------------------------------
echo '=> Install system utilities'
#sudo apt-get install -y .....whatever you want e.g. latex
echo 'Done.'

# -----------------------------------------------------------------------------
# => Install developer packages (python 3.5)
# -----------------------------------------------------------------------------
echo '=> Install developer packages'
sudo apt-get update
sudo apt-get install -y python3-pandas
sudo pip3 install pygsheets
sudo pip3 install configparser
sudo pip3 install adafruit-ads1x15
sudo pip3 install RPi.bme280
sudo pip3 install w1thermsensor
sudo pip3 install --upgrade pyasn1-modules
echo 'Done.'

# -----------------------------------------------------------------------------
# => Enable SSH and VNC
# -----------------------------------------------------------------------------

echo '>>> Enable SSH and VNC'
sudo raspi-config nonint do_ssh 0
sudo raspi-config nonint do_vnc 0

# -----------------------------------------------------------------------------
# => Configurations for serial, 1-Wire, I2C and UART
# -----------------------------------------------------------------------------

# enable 1-Wire GPIO on Raspberry Pi
echo '>>> Enable 1-Wire GPIO (w1)'
if grep -q 'dtoverlay=w1-gpio' /boot/config.txt; then
  echo 'Seems w1-gpio parameter already set, skip this step.'
else
  echo dtoverlay=w1-gpio >> /boot/config.txt
fi

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

#Stop Bluetooth modem to use UART
sudo systemctl disable hciuart

# -----------------------------------------------------------------------------
# => Create systemd unit file for hotplugging (mount/unmount) usb
# -----------------------------------------------------------------------------

#Create a script to run at power up
sudo cp /home/pi/relier/bash/usb-mount.sh /usr/local/bin/usb-mount.sh
sudo sed -i 's/\r//' /usr/local/bin/usb-mount.sh

#Call the script by a system unit file
sudo cp /home/pi/relier/services/usb-mount@.service /etc/systemd/system/usb-mount@.service

#Add the two rules (file 99-local.rules) to start and stop system unit service on hotplug/unplug
sudo echo 'KERNEL== "sd[a-z][0-9]", SUBSYSTEMS=="usb", ACTION=="add", RUN+="/bin/systemctl start usb-mount@%k.service"' >> /etc/udev/rules.d/99-local.rules
sudo echo 'KERNEL=="sd[a-z][0-9]", SUBSYSTEMS=="usb", ACTION=="remove", RUN+="/bin/systemctl stop usb-mount@%k.service"'>> /etc/udev/rules.d/99-local.rules

sudo udevadm control -l debug           #allows debugging (tail –f /var/log/syslog, and plug/unplug a usb stick)
sudo udevadm control --reload-rules     #reloads rules
sudo systemctl daemon-reload            #reloads systemd

#-----------------------------------------------------------------------------
# => Create systemd unit file to run at shutdown/reboot
# -----------------------------------------------------------------------------

#Create a script to run at shutdown/reboot
sudo cp /home/pi/relier/services/rcshut.service /etc/systemd/system/rcshut.service
sudo systemctl enable rcshut --now
sudo systemctl start rcshut
sudo chmod +w /home/pi/relier/shutdown.py

#-----------------------------------------------------------------------------
# => Create systemd unit file to control shutdown/restart button
# -----------------------------------------------------------------------------

#Create a script to run at shutdown/reboot
#sudo apt install python3-gpiozero this should be not needed because is already in raspbian now
sudo cp /home/pi/relier/services/shutdown_button.service /etc/systemd/system/shutdown_button.service
sudo systemctl daemon-reload
sudo systemctl enable shutdown_button --now
sudo systemctl start shutdown_button
sudo chmod +w /home/pi/relier/shutdown_button.py

# -----------------------------------------------------------------------------
# => Configurations of cron tab (files to run at startup)
# -----------------------------------------------------------------------------

# First remove all cron's
crontab -r

CMD="/usr/bin/pigpiod"
JOB="@reboot $CMD"
TMPC="mycron1"
sudo grep "$CMD" -q <(crontab -l) || (crontab -l>"$TMPC"; echo "$JOB">>"$TMPC"; crontab "$TMPC")
#
# -----------------------------------------------------------------------------
# => run main.py at start-up of raspberry pi (using a shell script in crontab)
# -----------------------------------------------------------------------------
# make the launcher script an executable
sudo chmod 755 /home/pi/relier/bash/launcher.sh
echo 'Create a logs directory'
sudo mkdir /home/pi/relier/logs
sudo chmod 777 -R /home/pi/relier/logs

CMD="sh /home/pi/relier/bash/launcher.sh >/home/pi/relier/logs/cronlog 2>&1"
JOB="@reboot $CMD"
TMPC="mycron2"
sudo grep "$CMD" -q <(crontab -l) || (crontab -l>"$TMPC"; echo "$JOB">>"$TMPC"; crontab "$TMPC")

# -----------------------------------------------------------------------------
# => Final reboot
# -----------------------------------------------------------------------------

if [ -f "/tmp/raspbian-post-install.sh" ]; then
sudo rm /tmp/raspbian-post-install.sh
fi
echo '>>> Rebooting'

sudo reboot