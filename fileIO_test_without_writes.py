import threading, thread
import yaml
import os
import json
import twitter
import time
import basic_sentiment_analysis
import signal
import sys

# Child: begins streaming tweets for a LOCATION
def child(location):
  # Keep track of local sentiment
  local_meter = 0

  # Used for graceful multi-fork kills in unix
  global killer

  i = 0 # used for analytics
  d=0
  start_time = time.time() # used for analytics
  for d in xrange(100000):
          
    if True:
      tweet = "placeholder"

      ## CRITICAL SECTION ###########
      global global_meter_lock
      with global_meter_lock:
        # update GLOBAL meter 
        update_global_meter(tweet)
      ###############################

      # gracefully kill thread if receive sigkill from terminal
      if killer.kill_now:
        break

  end_time = time.time()
  print "\n Location: " + location + " processing time: " + str(end_time-start_time) 

  return

# Parent: creates children, assigning map location (& API keys) from locations.yml
def parent():
  global global_meter
  global_meter = 0

  # code ripped from http://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
  global killer
  
  killer = GracefulKiller()
  threads = []
  file = open("dicts/locations.yml", 'r')

  # locations for each state generated from: http://tools.geofabrik.de/calc/
  global locations
  locations = yaml.load(file)

  # create a semaphore for the meter
  global global_meter_lock
  global_meter_lock = threading.Lock()

  # Generate thread to stream tweets from each state
  for location in locations:
    t = threading.Thread(target=child, args=(location,))
    threads.append(t)
    t.start()


  
  # Sit and let children do work, 
  # Occasionally updating the GLOBAL METER
  while True:
    time.sleep(1)
    
    ## CRITICAL SECTION ###########
    #update global meter
    global global_meter_lock
    with global_meter_lock:
      file_name = 'Global_meter.txt'
      wr = open(file_name, 'w')
      wr.write(str(global_meter))
      wr.close()  
    ###############################

    # Kill process gracefully if receive sigkill from user
    if killer.kill_now:
      break

# Updates global meter 
# ONLY TO BE CALLED IN CRITICAL SECTIONS
def update_global_meter(tweet):
  global global_meter
  value = 1
  global_meter = global_meter + value
  return str(global_meter)

# code ripped from http://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
# used because python isn't receiving sigkills from terminal on Ubuntu 16.04
class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

# Start!!!!
parent()