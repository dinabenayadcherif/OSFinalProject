import threading
import yaml
import os
import json
import twitter
import credentials
import time
import basic_sentiment_analysis

# Child: begins streaming tweets for LOCATION
def child(location):
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
      meter_lock.aquire()
      try:
        update_meter(tweet)
      finally: 
        meter_lock.release()
  return

# Parent: creates children, assigning map location (& API keys) from YAML
def parent():
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

def update_meter(tweet):
  global meter
  value = basic_sentiment_analysis.get_tweet_score(tweet)
  meter = meter + value

parent()