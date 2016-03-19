# rbSnapper

This package contains the control code for the Snapper robotic arm.

## Extra hardware

In addition to the Raspberry Pi, you'll need the following equipment (or equivalent):

-   6v Power Supply, such as: http://www.amazon.com/gp/product/B001BCOWLY?psc=1&redirect=true&ref_=oh_aui_detailpage_o04_s00
-   GPIO Breakout board, such as: https://www.sparkfun.com/products/13717
-   16 channel I2C Sevo Driver board from Adafruit: https://www.adafruit.com/products/815

## Preparing your Pi for i2c

Before using the library, you'll need to ensure that your Raspberry Pi is configured to talk to the servo driver board over i2c.

In `sudo raspi-config > Advanced Options` ensure that i2c support is enabled.  Reboot if necessary.

Run the following commands

    - sudo apt-get install python-smbus
    - sudo apt-get install i2c-tools

Check `/etc/modprobe.d/raspi-blacklist.conf` and ensure that `blacklist i2c-bcm2708'` is commented or removed

Edit `sudo nano /etc/modules` and add `i2c-bcm2708` and `i2c-dev`

Reboot

Once you have your i2c components connected to your Pi, run `sudo i2cdetect -y 1` for a Pi 2, or `sudo i2cdetect -y 0` on an older Pi

For the Adafruit 16 channel servo driver at the default address, the output of the above command should be:


     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- --
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    70: 70 -- -- -- -- -- -- --

This shows the driver connected to the Pi at address 40

NOTE: If you're using virtualenvwrapper to manage your Python environment, you'll need to make sure you have global site
packages available by running

    toggleglobalsitepackages

if necessary.

### Code setup

Obtain the driver library from Adafruit's Github account:

    git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git

To run the test code:

    cd Adafruit-Raspberry-Pi-Python-Code
    cd Adafruit_PWM_Servo_Drver

For our project we only need the following 2 files from the Adafruit code:

-   Adafruit_I2C.py
-   Adafruit_PWM_Servo_Driver.py