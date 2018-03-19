# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 18:55:25 2018

@author: aangris
"""

import time
import paho.mqtt.publish as publish
import linuxcnc
import linecache

s = linuxcnc.stat()

Broker = "iot.eclipse.org"

sub_topic = "sensor/instructions"    # receive messages on this topic

pub_topic = "LCNC/data"       # send messages to this topic


############### Linuxcnc inputs ##################
#Function to parse through the file being executed and display the gCode being run at the time it is accessed
def showGcode( Line,filename ):
    Gcode = linecache.getline(filename, Line)
    return Gcode

def status():
    s.poll()
    if getattr(s,'state')==2 and getattr(s,'interp_state')!=1:
        status = "cutting"
        GcodeLine=int(getattr(s,'id'))
        total_lines=s.read_line
        perc_complete = GcodeLine*100/total_lines
    else:
        status = "idle"
        perc_complete = 0
    
    return(perc_complete,status)


############### MQTT section ##################


while True:
    sensor_data = [status()]
    print sensor_data
    publish.single(pub_topic, str(status), hostname="iot.eclipse.org")
    time.sleep(0.1*60)
