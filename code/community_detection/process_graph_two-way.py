import glob
import os
import json
import sys
import csv
from collections import defaultdict

users = defaultdict(lambda: {'friends': 0})

for f in glob.glob('avbytes_twitter-users/*.json'):
	data = json.load(file(f))
	screen_name = data['screen_name']
	users[screen_name]['friends'] = data['friends_count']

SEED = 'avbytes'

def process_follower_list(screen_name,edges={},depth=0,max_depth=2):
	f = os.path.join('avbytes_following',screen_name + '.csv')

	if not(os.path.exists(f)):
		return edges

	with open(f, 'r') as outf:
	  reader = csv.reader(outf,dialect='excel')
	  friends = [row for row in reader]

	for friend_data in friends:
		if(len(friend_data) < 2):
			continue

		screen_name_2 = friend_data[1]

		weight = users[screen_name]['friends']

		if not((screen_name, screen_name_2) in edges.viewkeys()):
			edges[(screen_name, screen_name_2)] = weight

		if depth+1 < max_depth:
			process_follower_list(screen_name_2, edges, depth+1, max_depth)

	return edges

edges = process_follower_list(SEED, max_depth=4)
print "edges(set) is %d elements" % len(edges)

with open('edges.csv', 'w') as outf:
	writer = csv.writer(outf,dialect='excel')
	for edge in edges.iterkeys():
		out_param = (edge[0],edge[1], edges[edge])
		writer.writerow(out_param)

#needs testing
with open('twitter-network_two_way.csv','w') as outf:
	writer = csv.writer(outf,dialect='excel')
	for edge in edges.iterkeys():
		opp_edge = (edge[1],edge[0])
		print edge
		print opp_edge
		if opp_edge in edges:
			out_param = (edge[0],edge[1],edges[edge] + edges[opp_edge])
			writer.writerow(out_param)

"""
with open('twitter-network_two_way.csv','w') as outf:
	writer = csv.write(outf,dialect='excel')
	for edge in edges:
		new_param = (edge[1],edge[0],edge[2])
		if new_param in edges:
			writer.writerow(new_param)
			edges.discard(new_param)
"""
"""
with open('twitter-network_two_way.csv', 'w') as outf:
	writer = csv.writer(outf,dialect="excel")
	edge_exists = {}
	for edge in edges:
		key = ','.join([str(x) for x in edge])
		print key
		if not(key in edge_exists):
			writer.writerow(edge)
			#outf.write('%s\t%s\t%d\n' % (edge[0], edge[1], edge[2]))
			edge_exists[key] = True
		# writer.writerow(edge)
"""