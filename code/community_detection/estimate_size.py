import glob
import os
import csv

i = 0
for f in glob.glob('avbytes_following/*.csv'):
	with open(f, 'r') as read_f:
		reader = csv.reader(read_f)
		for row in reader:
			i += 1

i *= 3
print "The predicted number of requests are %d" % i

