import glob
import os
import json
import sys
import csv
from collections import defaultdict

users = defaultdict(lambda: {'followers': 0})

for f in glob.glob('uiuc_json/*.json'):
	data = json.load(file(f))
	screen_name = data['screen_name']
	users[screen_name]['followers'] = data['followers_count']

SEED = 'acmuiuc'

def process_follower_list(screen_name,edges=[],depth=0,max_depth=2):
	f = os.path.join('uiuc_members',screen_name + '.csv')

	if not(os.path.exists(f)):
		return edges

	#followers = []

	with open(f, 'r') as outf:
	  reader = csv.reader(outf,dialect='excel')
	  followers = [row for row in reader]

	for follower_data in followers:
		if(len(follower_data) < 2):
			continue

		screen_name_2 = follower_data[1]

		weight = users[screen_name]['followers']

		if screen_name != SEED and screen_name_2 != SEED:
			edges.append([screen_name, screen_name_2, weight])

		if depth+1 < max_depth:
			process_follower_list(screen_name_2, edges, depth+1, max_depth)

	return edges

edges = process_follower_list(SEED, max_depth=4)
# for edge in edges:
# 	print edge

with open('acm_edges1.csv', 'w') as outf:
	writer = csv.writer(outf,dialect="excel")
	edge_exists = {}
	for edge in edges:
		key = ','.join([str(x) for x in edge])
		# print key
		if not(key in edge_exists):
			writer.writerow(edge)
			#outf.write('%s\t%s\t%d\n' % (edge[0], edge[1], edge[2]))
			edge_exists[key] = True
		#writer.writerow(edge)
