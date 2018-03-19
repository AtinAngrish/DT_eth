# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:55:22 2018

@author: aangris
"""
import paho.mqtt.client as mqtt #import the client1
import tweepy
from ContractHandler import ContractHandler
import time

consumer_key = 'pTHSW5yxc0lipPvptsExXWkmI'
consumer_secret = 'YTXlvzvg3Qc2dprNIY8JPeg44yUllX4UPsgYk3GWHU4w3GpcmA'
access_token = '969665472043077633-AUMIeR6JrMfLKtg6sPSc97Wq099mFrQ'
access_token_secret = 'RLIpvvC5vupXvT5oGW05l8F4NefbSOHHGuSTJxk1NxI2e'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class stateWatcher:
    """ A simple class, set to watch its variable. """
    def __init__(self, value):
        self.variable = value
        self.ch_variable =value
        self.old = ""
        self.counter = 10
        self.CH = ContractHandler()
        self.CH.test()
        self.machine1_name = "CNC"
        self.machine1_mac = "AAA"
        self.machine1_time = 3
        self.machine1_rate = 1
#        self.CH.addUser()
#        self.CH.addMachine(self.machine1_name, self.machine1_mac, self.machine1_time, self.machine1_rate)
        print(self.CH.getMachineInfo(self.CH.mining_account,0))
    
    def set_value(self, new_value):
        start = time.time()
        if self.variable != new_value:
            self.old = self.variable
            self.variable =new_value
            self.ch_variable = self.old
            delta = time.time() - start
            self.on_change(delta)
        else:
            pass
              
    def on_change(self,delta):
        # do stuff when variable changed
        if self.variable=="idle":
            self.counter+=1 
            # We are updating only the state of the machine on the chain for now
            self.CH.updateMachineStatus(self.CH.mining_account, 
                                        self.machine1_mac, 
                                        True, 
                                        self.machine1_time,
                                        self.machine1_rate)
            #while not self.CH.getMachineInfo(self.machine1_mac, 0):
            #    pass #this will stall the program until the transaction is recorded in a block
            tweet = "Update# "+str(self.counter) + " : I am now available!"
            print(tweet)
            api.update_status(status=tweet)
        elif self.variable=="cutting":
            self.counter += 1
            self.CH.updateMachineStatus(self.CH.mining_account
                                        , self.machine1_mac
                                        , False
                                        , self.machine1_time
                                        , self.machine1_rate)
            #while self.CH.getMachineInfo(self.machine1_mac, 0):
            #    pass #this will stall the program until the transaction is recorded in a block
            tweet = "Update# "+str(self.counter) + " : I am now busy executing order from "+self.CH.trading_account
            print(tweet)
            api.update_status(status=tweet)

        #tweet = "I am now "+self.variable

Broker="iot.eclipse.org"
sub_topic = "LCNC/data"       # send messages to this topic
pub_topic = "LCNC/commands"
state = stateWatcher('idle')
# when connecting to mqtt do this;
prev = "idle"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topic)
# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    message = str(msg.payload)
    #print(msg.topic+" "+message)
    mach_status=str(message)
    #print(mach_status)
    state.set_value(mach_status)
    print(mach_status)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))
while True:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect(Broker, 1883, 60)
    
    client.loop_forever()
