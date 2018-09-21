#!/usr/bin/env python2.7

import logging
logging.basicConfig(filename='stravascrollerLog.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
import stravalib #sudo pip install stravalib
import math
import scrollphat #curl -sS https://get.pimoroni.com/scrollphat | bash
import time
import datetime
import sys

logging.debug('Start of program')

scrollphat.set_brightness(14)
scrollphat.set_rotate(True)
client = stravalib.client.Client(access_token="your-api-key-goes-here") # replace this with your Strava API key
#Getting token: https://pythonhosted.org/stravalib/usage/auth.html

km_per_pixel = 5.0 #each pixel in the chart represents this many km in the activity, rounded up to the next pixel
tickduration = 0.12 #seconds delay per tick
ticks_per_second = 1/tickduration
strava_refresh_interval_secs = 60*10 #poll strava every 10 minutes, 60*10 seconds in between updates
screen_switch_interval_secs = 7 # change screens every X seconds

stravarefreshtimeout = ticks_per_second * strava_refresh_interval_secs
screenswitchtimeout = ticks_per_second * screen_switch_interval_secs
totalscreens = 2
totaldistance = 0

today = datetime.date.today()
monday = today - datetime.timedelta(days=today.weekday())
mondaypst = str(monday) + "T07:00:00Z"

# Create race day countdown timer
todayDate = datetime.datetime.now()
raceDay = datetime.datetime(2018, 06, 17)
delta = raceDay - todayDate
daysLeft = delta.days

def sortby(item):
    return item.start_date

def getstravabargraph():
    global totaldistance
    totaldistance = 0
    activitiesthisyear = client.get_activities(after = mondaypst, limit=500) # Download all activities this year

    for activity in activitiesthisyear:
        totaldistance += float(stravalib.unithelper.miles(activity.distance)) #add up the total distance

    limit = 0
    bargraph = []
    #Get the most recent 5 activities to draw the bar chart
    for activity in sorted(activitiesthisyear, key=sortby, reverse=True):
        bargraph.append(int(math.ceil(float(stravalib.unithelper.miles(activity.distance)) / km_per_pixel)))
        limit += 1
        if limit == 5: #only get most recent 5 activities (1 per row of pixels)
            break

    bargraph.reverse()
    return bargraph

# def drawgraph(values):
    scrollphat.clear_buffer()
    for row, value in enumerate(values):
        for col in range(0,11):
            if value<=col:
                scrollphat.set_pixel(col,row,False)
            else:
                scrollphat.set_pixel(col, row, True)
    scrollphat.update()

stravatimer = 0
screentimer = 0
screen = 0

scrollphat.clear() #clear the display

# Sleep for 10 seconds to give the wifi connection time to connect while showing loading pattern
for i in range(0,10):
    scrollphat.set_pixels(lambda x, y: x<=i, True)
    scrollphat.update()
    time.sleep(1) # wait 1 second

scrollphat.set_pixels(lambda x, y: (x + y) % 2, True) #set chequer pattern while Strava is loading
bargraph = getstravabargraph() # Get an initial load from Strava

print ("Running...")
while True: #Loop this bit forever
    try:
        time.sleep(tickduration)

        if screen==0:
#            show the number of days left until race
            scrollphat.write_string("%.0f" % daysLeft) #Show days until race on screen

        if screen==1:
            scrollphat.write_string("%.0f" % totaldistance) #Show the total distance on the screen

        if(stravatimer > stravarefreshtimeout): # Time to refresh data from Strava
            scrollphat.set_pixels(lambda x, y: (x + y) % 2, True)  # set chequer pattern to show loading
            bargraph = getstravabargraph()
            scrollphat.clear()
            stravatimer = 0
        else:
            stravatimer = stravatimer+1

        if (screentimer > screenswitchtimeout): # Time to move to the next screen
            screen = (screen + 1) % (totalscreens)
            screentimer = 0
            scrollphat.clear()
        else:
            screentimer = screentimer + 1

    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)
