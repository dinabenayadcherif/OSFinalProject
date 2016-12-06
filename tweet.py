import os
import json
import twitter
import credentials
import time
import basic_sentiment_analysis
#TODO:

#SPLIT INTO FORKED PROCESSES

#FOR EACH LOCATION X
  #Stream tweets from location X
  #Check Tweet against slur library
  #Return score
  #Edit location X running score
  #Edit global running score

def main():
  initialize_t()
  stream_tweets_to_file()

def initialize_t():
  USERS = ['@twitter', '@twitterapi', '@support']
  LANGUAGES = ['en']

  #Open API
  global api
  api = twitter.Api(credentials.consumer_key, credentials.consumer_secret, credentials.access_token_key, credentials.access_token_secret)
  
  #Set location 
  global location
  location = [[],[]]
  global COORDINATES, NAME
  COORDINATES = 0
  NAME = 1
  #Shoutout to BoundingBox:  http://boundingbox.klokantech.com/
  location[COORDINATES] = ["-81.8791, 41.333","-81.4698, 41.5685"] #Cleveland area location
  location[NAME] = "Cleveland"

  #set up score meter
  global meter
  meter = 0
  global love_meter
  love_meter = 0
  global hate_meter
  hate_meter = 0

def stream_tweets_to_file():
  #Name File
  file_name = "".join(location[NAME]) + '_tweets.txt'

  #MEMORY MANAGEMENT: AVOIDING MULTIPLE-READ-WRITES FOR EACH PROCESS
  #for each tweet received, write to file
  for line in api.GetStreamFilter(locations=location[COORDINATES]):
    if 'text' in line:
      #get tweet
      tweet = json.dumps(line["text"])

      #critical section: file access
      f = open(file_name, 'a')
      f.write(tweet + '\n')
      f.close()
      #end critical section

      #update naught meter
      update_meters(tweet)

      global meter
      print "A tweet was received! New scores: "
      print "hate " + str(hate_meter) + "| love " + str(love_meter)+ " | total " + str(meter)

#updates global "meter" variable with new value
def update_meters(tweet):
  global meter
  global love_meter
  global hate_meter

  value = basic_sentiment_analysis.get_tweet_score(tweet)
  global meter
  meter = meter + value

  if (value < 0):
    hate_meter -= hate_meter

  if (value > 0):
    love_meter += love_meter



if __name__ == '__main__':
  main()
