import threading
import yaml
import os
import json
import twitter
import credentials
import time
import basic_sentiment_analysis

#Child: begins streaming tweets for LOCATION
def child(location):
  global locations
  print "location: " + location  + " coordinates: " + str(locations[location])
  # put into twitter-api-friendly format
  coordinates = [locations[location][0], locations[location][1]]

  for line in api.GetStreamFilter(locations=coordinates):
    if 'text' in line:
      #get tweet
      tweet = json.dumps(line["text"])
      print tweet
  return

#Parent: creates children, assigning map location (& API keys?)
def parent():
  threads = []
  file = open("dicts/locations.yml", 'r')

  #locations for each state generated from: http://tools.geofabrik.de/calc/
  global locations
  locations = yaml.load(file)

  global api
  api = twitter.Api(credentials.consumer_key, 
      credentials.consumer_secret, 
      credentials.access_token_key, 
      credentials.access_token_secret)

  # Generate thread to stream tweets from each state
  for location in locations:
    t = threading.Thread(target=child, args=(location,))
    threads.append(t)
    t.start()

parent()