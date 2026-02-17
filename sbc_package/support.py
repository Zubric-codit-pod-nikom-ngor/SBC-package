import os
def get(filename):
	this_file = os.path.abspath(__file__)
	this_dir = os.path.dirname(this_file)
	wanted_file = os.path.join(this_dir, filename)
	return wanted_file

