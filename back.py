# -*- coding: utf-8 -*-
"""
Created on Sun May 20 09:47:09 2018

@author: jure
"""

import webbrowser
import os
import serial, time

url = "http://127.0.0.1:5000"
url2 = url + "/index_office"

# Open URL in a new tab, if a browser window is already open.
#webbrowser.open_new_tab(url + 'doc/')

# Open URL in new window, raising the window if possible.
webbrowser.open_new(url)





ser = serial.Serial('/dev/ttyACM0', 9600)
print(ser.name)   

while 1:
    serial_line = ser.readline()

#    print((serial_line[0]) # If using Python 2.x use: print serial_line
    # Do some other work on the data
    if serial_line[0] == 85:
        webbrowser.open_new(url2)

    time.sleep(0.2) # sleep 5 minutes

    # Loop restarts once the sleep is finished

ser.close() # Only executes once the loop exits