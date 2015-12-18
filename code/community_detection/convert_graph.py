import networkx as net
from networkx.readwrite import json_graph
import community as comm
import csv
import os
import json
import sys
import igraph
import infomap
import pygraphviz

g = net.read_pajek('/Users/arvind/Documents/College_2015/socialmedia_power/code/Infomap/infomap_output/acm_outdirdir_mapgen_export.net')

def write_json(gIn, fname):
	d3data = json_graph.node_link_data(gIn)
	with open(fname,'w') as outf:
		json.dump(d3data,outf)

write_json(g,'test_source.json')

if os.path.exists('test_source.json'):
	print "Success! One file written!"