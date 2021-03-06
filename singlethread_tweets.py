import yaml
import os
import json
import twitter
import time
import itertools
import basic_sentiment_analysis


def main():
  global meter
  meter = 0

  file = open("dicts/locations.yml", 'r')

  # locations for each state generated from: http://tools.geofabrik.de/calc/
  global locations
  locations = yaml.load(file)

  # Cycle through each state
  for location in itertools.cycle(locations):

    # put into twitter-api-friendly format
    coordinates = [locations[location][0], locations[location][1]]

    # Open API connection
    global api
    api = twitter.Api(locations[location][2],
        locations[location][3],
        locations[location][4],
        locations[location][5])
    i = 0
    start_time = time.time()

    # loop run with each new tweet
    for line in api.GetStreamFilter(locations=coordinates):
      if i >= 20:
        end_time = time.time()
        print "\nLocation: " + location + " processing time: " + str(end_time-start_time) + "for 20 tweets."
        break
      else: 
        if 'text' in line:
          tweet = json.dumps(line["text"])
          print "\n[location: " + location + "] tweet: " + tweet

          value = basic_sentiment_analysis.get_tweet_score(tweet)
          meter = meter + value
          meter2 = str(meter)

          file_name = location + '_meter.txt'

          wr = open(file_name, 'w')
          wr.write(meter2)
          i += 1

def update_meter(tweet):
  global meter
  value = basic_sentiment_analysis.get_tweet_score(tweet)
  meter = meter + value
  return str(meter)

main()
