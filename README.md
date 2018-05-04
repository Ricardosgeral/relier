# *erosLab* 
# Laboratory Erosion Test Software 
Open design of a sensor acquisition system of a laboratory erosion test apparatus, using a *Raspberry Pi* as server, and *Python* code. 

This work has been done by **Ricardo Correia dos Santos** at [Laboratório Nacional deEngenharia Civil - LNEC](http://www.lnec.pt/en/), in Lisbon, Portugal.

**Project Webpage**: https://ricardosgeral.github.io/erosLab/

#### Is this for me ?
You just need to have some DIY skills, for scrapping some materials, figuring out 
how to assemble some things together, and figuring out how some components work. The 
instructions given here should also be taken more like guidelines based on what 
I could do with the materials I had. If you do not have the exact same hardware
(sensors, ADC, level shifter, touchscreen...), they'll surely work a little different, but as they should do the same 
things, there will be similarities too. 

Feel free to contact me if you manage to get it working with different components, 
so these instructions can be improved and be more helpful. 

# Software (running in the *Raspberry Pi*)

## Installation
These instructions should be carried out after a fresh installation of *Raspbian* image (see [instructions](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)). In this project I've used [2018-04-18-raspian-stretch](http://downloads.raspberrypi.org/raspbian/images/raspbian-2018-04-19/). 
The generality of the code was done in *Python 3.5*. A few scripts were written in *Bash*.

**NOTE:** If no monitor is available (headless *Raspberry Pi*), you have to do the following 4 simple steps to enable *SSH* in first boot. So, right after installing the raspbian image in the  Micro SD card:
1. Create an empty file (in Windows use notepad, in a Linux terminal use command *touch*, in Mac use TextEdit).
2. Save the file with name: **ssh** (preferentially with no extension, but *ssh.txt* should also work).
3. Copy or move the ssh file into the *Root* of the Micro SD card.
4. Insert the Micro SD card in the *Raspberry Pi*, and power it on.

Connect to *Raspberry Pi* directly (if monitor is available) or via *SSH* (for example, using *Putty*). In this last option, you need to know the IP of the raspberry pi!

It is recommended to change the password in first boot, since *SSH* is enabled!

    $ passwd 
    
   **Login**: *pi*
   
   **Password**: *raspberry*

In a terminal, run the following sequential commands:
    
    $ cd /tmp && wget https://raw.githubusercontent.com/Ricardosgeral/erosLab/master/bash/raspbian-post-install.sh
    $ sudo chmod +x raspbian-post-install.sh
    $ sed -i 's/\r//' raspbian-post-install.sh
    $ sudo ./raspbian-post-install.sh

Next, you need to create your own JSON file with the google credentials
To obtain the credentials, follow instructions on this [Link](https://pygsheets.readthedocs.io/en/latest/authorizing.html#signed-credentials). 
Once you generated the JSON file, edit the dummy file in the Raspberry Pi:

    $ sudo nano /home/pi/erosLab/service_creds.json
    
Delete all content of the file and past your own credentials. Ctrl+X, yes and Enter to save file.

    $ sudo reboot

And that's it, after reboot, the *Raspberry Pi* server should be running properly, if **hardware** is also set correctly!

# Hardware

In this section there are indicated all the hardware items required to put the server running and capturing the sensors readings. 
It is also indicated the way those pieces should be connected.
Just for a reference about the cost of the project, some links and prices of the components are also presented.

## (Micro)computer and necessary components

+ 1x [**Raspberry Pi 3 model B**](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) [35€]
+ 1x [Micro SD card (>=8Gb - I´ve used one with 32Gb)](https://www.aliexpress.com/item/SAMSUNG-Micro-SD-Card-256G-128GB-64gb-32g-100M-s-Class10-U3-4K-UHD-Memory-card/32813615707.html?spm=a2g0s.9042311.0.0.Xdt3Ob) [12 €]
+ 1x [Raspberry Pi Universal Power Supply or equivalent](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/) [15€]
+ 1x [Raspberry Pi GPIO 40 pin cable](https://www.aliexpress.com/item/Raspberry-pi-B-raspberry-PI-GPIO-40-pin-cable/32809594049.html?spm=2114.search0104.8.35.5790121bpoCIAu&transAbTest=ae803_2&priceBeautifyAB=0) [3€]
+ 1x [Raspberry Pi case](https://www.aliexpress.com/item/Best-Selling-Clear-Case-for-Raspberry-Pi-3-Model-B-Clear-by-SB-Components-Plastic-Protective/32738665641.html?spm=a2g0s.9042311.0.0.A8JBGc) [2€] (optional!)


## Acquisition system box developed to read the sensors

+ 1x **PCB with 2 layers** (details to manufacter the *PCB* are shown below) [12 €]
+ 1x [**Nextion touchscreen 2.8"** - NX3224T028](https://nextion.itead.cc/shop-nextion/) [15 €]
+ 1x [**16 Bit I2C ADS1115** Module ADC 4 channel with Pro Gain Amplifier](https://www.aliexpress.com/item/16-Bit-I2C-ADS1115-Module-ADC-4-channel-with-Pro-Gain-Amplifier-RPi-1PCS/32817162654.html?spm=a2g0s.9042311.0.0.KZKf8O) [2€]
+ 1x [**Logic Level Shifter** Bi-Directional 5V to 3.3V](https://www.aliexpress.com/item/5PCS-Logic-Level-Shifter-Bi-Directional-For-Arduino-5V-to-3-3V-Four-Way-Two-Way/32827270848.html?spm=a2g0s.9042311.0.0.PRV9iC) [2€]
+ 1x [88x38x100mm aluminum box profile with enclosure for PCB](https://www.aliexpress.com/item/Free-shipping88-38-100mm-width-x-high-x-length-aluminum-extrusion-box-profile-enclosure-for-PCB/32800855972.html?spm=a2g0s.9042311.0.0.Wvmz38) [6€]
+ 6x [8mm Male & Female Connector miniature Aviation Plug M8 Circular Socket+Plug](https://www.aliexpress.com/item/1PCS-AP049-YC8-2-3-4-5-6-7Pin-8mm-Male-Female-Connector-miniature-Aviation-Plug/32845374887.html?spm=a2g0s.9042311.0.0.6sphAY) [6x4=24€]
+ 6x [XH2.54 3-Pins connectors with right angle Male for PCB - Header+Housing+Terminal](https://www.aliexpress.com/item/XH2-54-2P-3P-4P-5P-6P-7P-8P-9P-10P-11P-12P-13P-14P-15P/32793262315.html?spm=a2g0s.9042311.0.0.DEz5gr) [3€]
+ 1x [2.54mm 2x20 DC3 40 Pin Right Angle Male for PCB](https://www.aliexpress.com/item/10pcs-2-54mm-2x20-DC3-40-Pin-Right-Angle-Male-Shrouded-PCB-IDC-Socket-Box-header/32597308721.html?spm=a2g0s.9042311.0.0.y1HFgb) [4€]
+ 1x [Momentary pushbutton switch 3A Reset Button](https://www.aliexpress.com/item/10pcs-Momentary-Push-Button-Switch-12mm-Momentary-pushbutton-switches-3A-125VAC-1-5A-250VAC-Reset-Button/32802331189.html?spm=a2g0s.9042311.0.0.1PWJGq) [2€]
+ 1x 3mm LED [<1€]
+ 1x Active Buzzer Alarm 5V  [<1€]
+ 3x 10kΩ carbon film resistor [<1€]
+ 1x 20kΩ carbon film resistor [<1€]
+ 1x 4 pins Male Single Row Pin Header Strip [<1€]
+ 6 x 4cm *shielded* cable with 3 wires [<1€]

## Printed circuit board (*PCB*) designed/produced
The design of the 2 layer's *PCB* was developed using [Fritzing](http://www.fritzing.org/). 
It's production files and the *.fzz* file are [here](https://github.com/Ricardosgeral/erosLab/tree/master/Fritzing). 
The *PCB* was printed by [PCBWay company](https://www.pcbway.com/).

Below, you can see images showing the circuits hooked in the breadboard and in the PCB, as well as the final aspect of each layer individually.

**Fritzing Breadboard view**
![Breadboard_image](Fritzing/breadboard_erosLab.JPG)

**Fritzing PCB view**
![PCB_image](Fritzing/PCB_erosLab.JPG)

**Look of the PCB top layer**

![FinalPCBtop_image](Fritzing/Final_TopPCB_erosLab.JPG)

**Look of the PCB Bottom Layer**

![FinalPCBbottom_image](Fritzing/Final_bottomPCB_erosLab.JPG)


## Sensors

The following **'low cost' sensors** were used:
+ 3x [**Pressure Transducer Transmitter Sensor**, 0-5psi 5V](https://www.aliexpress.com/item/1Pc-Pressure-Transducer-Sender-Stainless-Steel-for-Oil-Fuel-Air-Water-5psi-CSL2017/32814346612.html?spm=2114.search0104.3.34.61855791WWOsT5&ws_ab_test=searchweb0_0,searchweb201602_1_10152_10151_10065_10344_10068_10342_10343_5722611_10340_10341_10698_10696_5722911_5722811_10084_5722711_10083_10618_10304_10307_10301_5711211_10059_308_100031_10103_10624_10623_10622_10621_10620_5711311_5722511,searchweb201603_32,ppcSwitch_5&algo_expid=a59a0ef4-feff-4b1a-b341-8883ad49d5dc-5&algo_pvid=a59a0ef4-feff-4b1a-b341-8883ad49d5dc&transAbTest=ae803_2&priceBeautifyAB=0) [3x13=39€]
+ 1x [**Turbine flow sensor**, 1.5" DN40 2~200L/min water Plastic Hall ](https://www.aliexpress.com/item/1-5-DN40-2-200L-min-water-Plastic-Hall-Turbine-flow-sensor-industry-meter/32445746581.html?spm=a2g0s.9042311.0.0.lPAUbg) [13€]
+ 1x [**Analog Turbidity Sensor**, 5V 40mA](https://www.aliexpress.com/item/DFRobot-Gravity-Analog-Digital-Turbidity-Sensor-5V-40mA-DC-support-both-signal-output-compatible-with-arduino/32595773560.html?spm=a2g0s.9042311.0.0.dGtxdp) [9€]
+ 1x [Waterproof DS18B20 digital temperature sensor (probe)](https://www.aliexpress.com/snapshot/0.html?spm=a2g0s.9042311.0.0.oXghXt&orderId=505161631680030&productId=32675444739) [<1€]
+ 1x [BME280 Digital Sensor, Humidity Temperature and Barometric Pressure Sensor](https://www.aliexpress.com/item/3In1-BME280-GY-BME280-Digital-Sensor-SPI-I2C-Humidity-Temperature-and-Barometric-Pressure-Sensor-Module-1/32659765502.html?spm=a2g0s.9042311.0.0.oXghXt) [3€]

Majority of the sensors are connected to the Acquisition system box via the mini aviator plugs. An exception is the *BME280* chip, which is soldered directly into the PCB.

## Other components that may be useful
+ Breadboard(s)
+ [T-cobbler for raspberry pi](https://www.aliexpress.com/item/830-tie-points-MB102-breadboard-40Pin-Rainbow-Cable-GPIO-T-Cobbler-Plus-Breakout-Board-Kit-for/32673580640.html?spm=2114.search0104.3.9.6581309ai8NJdY&ws_ab_test=searchweb0_0,searchweb201602_1_10152_10151_10065_10344_10068_10342_10343_5722611_10340_10341_10698_10696_5722911_5722811_10084_5722711_10083_10618_10304_10307_10301_5711211_10059_308_100031_10103_10624_10623_10622_10621_10620_5711311_5722511,searchweb201603_32,ppcSwitch_5&algo_expid=3ed88c37-67f1-4fe2-a688-b3983db90ff7-1&algo_pvid=3ed88c37-67f1-4fe2-a688-b3983db90ff7&transAbTest=ae803_2&priceBeautifyAB=0)
+ DuPont jumper wires
+ Micro SD adapter

## Additional tools required for the assemblage of the PCB and acquisition system
+ Cable wire Stripper/Crimping Plier
+ Soldering iron + sold
+ Tools to make the openings in the aluminum box (*e.g.* a mini Drill DIY set should be enough) 
+ Precision screwdriver set

# Usage of the Graphical User Interface (GUI)
 
Here are presented the pages GUI displayed in the touchscreen monitor (Nextion device).

**Credits**
 
![page1](Nextion/320x240/Artboard_1.png)
 
 **Main**
 
![page2](Nextion/320x240/Artboard3.png)
 
**General settings**
 
![page3](Nextion/320x240/settings0.bmp)

**Test Type selection**
 
![page4](Nextion/320x240/Artboard5a.png)

**Analog sensors config**
 
![page5](Nextion/320x240/Artboard7.png)

**Record readings**
 
![page6](Nextion/320x240/Artboard9.png)

**Stop recording readings**
 
![page7](Nextion/320x240/Artboard11.png)

**Disconnect indication**

![page0](Nextion/320x240/shutdown.bmp)

# Data collection
The *Raspberry Pi*, together with the *acquisition system box*, handles the sensors and gets the data from them. 
The data is collected once the red button in the *touchscreen GUI* (in *Sensors* page) is pressed. 
The location where data will be collected depends on the user *settings*, on whether an internet connection is available and a USB drive is plugged in.

## No internet connection
The data has two possible ways to go:
  
1. **No** USB drive is plugged in
   
   Data are stored *only* locally on the Micro SD card. The data are stored in the *CSV* format inside folder **/srv/EROSTESTS**. 

2. A USB is plugged in (before recording data!)

   Data are stored *only* on **USB_root_directory** in the *CSV* format. 

**Additional notes:**

- The name of the *CSV* file is defined by the user, either using:
   + the *touchscreen GUI* in *Settings page*, or  
   + the *inputs.ini* file, modifying the parameter *filename*.

- Before removing a USB drive or the Micro SD card it is **strongly** recommended to gently shutdown the *Raspberry Pi* and unplug the power supply.
This will prevent corrupting the Micro SD card and the USB drive. For that you can either:
   + press the *red pushbutton* in the back of the *acquisition system box* for more than *7 seconds*, or 
   + *$ sudo halt* in a *SSH* terminal session.
- If more than one USB drive is plugged in (not recommended!), data will be saved in the *first drive* being found.
- Data in the *CSV* files is never deleted automatically. If the filename already exists in the USB drive or Micro SD card, data is placed bellow the last row present. This means that multiple tests may be collected in the same filename (not recommended!).


## Internet connection available

The *local data* collection method is identical as stated when there is no internet connection.
That is, if a USB drive is plugged in, data goes to USB, otherwise, data goes to the Micro SD card.

**In addition**, it is possible to send data to [Google Sheets](https://www.google.com/sheets/about/), if a valid *service_creds.JSON* file is provided (see instructions in *Software>Installation* section).
With this functionality, you can do **Live monitoring** of the data being placed in the internet. 

**To enable 'Google sheets'**
-  Select the appropriate option:
   + In the *touchscreen GUI* > *Settings* page > activate the (only) checkbox. 
   + In *inputs.ini* file > ensure that *google_sheets = yes*.
   
- Provide a Tittle for the *Spreadsheet* and a Tittle for the *Worksheet*:
   + In the *touchscreen GUI* > *Settings* page > Add Tittle for spreadsheet (the worksheet name will be the tittle of the CSV filename).
   + In *inputs.ini* file > spreadsheet name is defined by parameter *googlesh* and worksheet name by *filename*.

- Provide a valid email, since a link to access the spreadsheet will be shared via email at the start of each test
   + In the *touchscreen GUI* > *Settings* page > Add email
   + In *inputs.ini* file > use parameter *share_email*

**Additional notes:**

- If the spreadsheet/worksheet provided by the user already exists, the data that was in that worksheet will be deleted (**Attention!**). 
However, when a new worksheet name is provided in an already existing spreadsheet, a new sheet is added. 
This means that you can have a single spreadsheet with different tests organized in different worksheets.
- If internet connection is lost during a test, the software will raise an error and stop recording data! (**be careful!**).

# Troubleshooting

- The following warning is expected: 'grep: /dev/fd/63: No such file or directory' at the end of $ *sudo ./raspbian-post-install.sh*.
- Don't forget to obtain and replace the content of the file **service_creds.json**, as indicated above, or the program will not start!
- The inspection of the **cronlog** file ($ *sudo nano /home/pi/erosLab/logs/cronlog*) may be helpful for detecting any eventual bugs during the software installation process.
- To check if the *Analog-to-Digital Converter* (ADC - ADS1115 chip) is properly connected via I2C, you can do **$ cd sudo i2cdetect -y 1**. 
 You should see number **48** in the matrix (row 40, column 8). 
 Otherwise, something is not connected correctly, or I2C protocol has not been enabled (the bash file *raspbian-post-install.sh* run in installation is supposed to do that).

# Licence
Please see the [licence conditions](LICENSE).