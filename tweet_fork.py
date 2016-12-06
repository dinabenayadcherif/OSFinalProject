import os

num_locations = 10

def child():
	print('\n a new child! ', os.getpid())
	get_location()
	os._exit(0)

def parent():
	global num_locations

	for location in xrange(num_locations):
		newpid = os.fork()
		if newpid == 0:
			child()
		else:
			pids = (os.getpid(), newpid)
			print("parent: %d, child: %d\n" % pids)
		




parent()