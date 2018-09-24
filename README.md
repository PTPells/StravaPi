# StravaPi

*How many miles have you run so far this week?*
*How many days until your next race?*

This script visualizes both data points on a little [LED matrix](https://www.adafruit.com/product/3473), powered by a [Raspberry Pi Zero](https://www.adafruit.com/product/3400).

![alt text](https://github.com/PTPells/StravaPi/blob/master/stravapi.jpg)

## What does this do?

This script will automatically pull and visualize your Strava running stats on a [Scroll pHAT LED matrix](https://www.adafruit.com/product/3473), atop a little [Raspberry Pi Zero](https://www.adafruit.com/product/3400). 

Right now, the LED displays two data points: 
1) Your total miles run since the beginning of the week  
2) The number of days remaining until your next race (or any date you define)


## Components

* [Stravalib](https://pythonhosted.org/stravalib/api.html?highlight=client#module-stravalib.client)
* [Scroll pHat](https://shop.pimoroni.com/products/scroll-phat)
* [Raspbery Pi Zero](https://www.raspberrypi.org/products/raspberry-pi-zero/)


## Creating your own

See @solipsia's [excellent] Instructables [tutorial](http://www.instructables.com/member/solipsia/).
