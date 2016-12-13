import threading, thread
import yaml
import os
import json
import twitter
import time
import basic_sentiment_analysis
import signal
import sys

# Child: begins streaming tweets for LOCATION
def child(location):
  global killer
  global locations
  # put into twitter-api-friendly format
  coordinates = [locations[location][0], locations[location][1]]


  # Open API connection
  global api
  api = twitter.Api(locations[location][2], 
      locations[location][3],
      locations[location][4],
      locations[location][5])

  # loop run with each new tweet
  for line in api.GetStreamFilter(locations=coordinates):
    if 'text' in line:
      tweet = json.dumps(line["text"])
      print "\n[location: " + location + "] tweet: " + tweet
      
      #CRITICAL SECTION
      global meter_lock
      with meter_lock:
        meter = update_meter(tweet)

      file_name = location + '_meter.txt'
      wr = open(file_name, 'w')
      wr.write(meter)  

      # gracefully kill thread if receive sigkill from terminal
      if killer.kill_now:
        break

  return

#analyzes velocity of hate per 10 seconds
def meter_maid():
  time.sleep(10)

  global global_meter_lock
  with global_meter_lock:
    meter = 0
  #CRITICAL SECTION
    #global meter_lock
    #  with meter_lock:
    #    meter = update_meter(tweet)

   #    file_name = location + '_meter.txt'
     #  wr = open(file_name, 'w')
       #wr.write(meter)  


# Parent: creates children, assigning map location (& API keys) from YAML
def parent():
  global meter
  meter = 0

  threads = []
  file = open("dicts/locations.yml", 'r')

  # locations for each state generated from: http://tools.geofabrik.de/calc/
  global locations
  locations = yaml.load(file)

  # create a semaphore for the meter
  global meter_lock
  meter_lock = threading.Lock()

  # Generate thread to stream tweets from each state
  for location in locations:
    t = threading.Thread(target=child, args=(location,))
    threads.append(t)
    t.start()

  # code ripped from http://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
  global killer
  killer = GracefulKiller()

  while True:
    time.sleep(1)
    if killer.kill_now:
      break

def update_meter(tweet):
  global meter
  value = basic_sentiment_analysis.get_tweet_score(tweet)
  meter = meter + value
  return str(meter)


class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

parent()