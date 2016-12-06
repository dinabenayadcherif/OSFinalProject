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
	#locations for eaach state from: http://tools.geofabrik.de/calc/#type=geofabrik_standard&bbox=-84.820337,38.403142,-80.518991,42.323237&tab=1&proj=EPSG:4326&places=2
  #print "location: " + location  + " coordinates: " + str(locations[location])
  print "loc: "+ locations[0]
	#Open API

'''	global api

	for line in api.GetStreamFilter(locations=location):
	  if 'text' in line:
	    #get tweet
	    tweet = json.dumps(line["text"])
*/
  return '''

#Parent: creates children, assigning map location (& API keys?)
def parent():
	threads = []
	file = open("dicts/locations.yml", 'r')

"""	global api
    api = twitter.Api(credentials.consumer_key, 
    	credentials.consumer_secret, 
    	credentials.access_token_key, 
    	credentials.access_token_secret)
"""
	global locations
	locations = yaml.load(file)

	for location in locations:
		t = threading.Thread(target=child, args=(location,))
		threads.append(t)
		t.start()

parent()