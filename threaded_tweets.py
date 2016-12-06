import threading
import yaml

#Child: begins streaming tweets for LOCATION
def child(location):
	global locations
	print "location: " + location + " coordinates: " + str(locations[location])
	return

#Parent: creates children, assigning map location (& API keys?)
def parent():
	threads = []
	file = open("dicts/locations.yml", 'r')

	global locations
	locations = yaml.load(file)

	for location in locations:
		t = threading.Thread(target=child, args=(location,))
		threads.append(t)
		t.start()

parent()