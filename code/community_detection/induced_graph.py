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
from cocotools import infomap as ifmap


from collections import defaultdict
import math

twitter_network = []

with open('acm_edges1.csv') as f_datin:
    reader = csv.reader(f_datin,dialect='excel')
    twitter_network = [row for row in reader]

o = net.MultiDiGraph()
hfollowers = defaultdict(lambda: 0)
for (twitter_user, followed_by, followers) in twitter_network:
    #o.add_edge(twitter_user, followed_by)
    name_user = "U: " + twitter_user
    name_follower = name = "U: " + followed_by
    o.add_edge(name_user, name_follower, followers=int(followers))
    hfollowers[name_user] = int(followers)

SEED = 'acmuiuc'

def trim_degrees(gIn, degree=1):
    g2 = gIn.copy()
    d = net.degree(g2)
    for n in g2.nodes():
        if n == SEED: continue # don't prune the SEED node
        if d[n] <= degree:
            g2.remove_node(n)
    return g2

def trim_edges(gIn, weight=1):
    g2 = net.MultiDiGraph()
    for f, to, edata in gIn.edges_iter(data=True):
        if f == SEED or to == SEED: # keep edges that link to the SEED node
            #g2.add_edge(f, to, weight=edata)
            g2.add_edge(f,to)
        elif edata['followers'] >= weight:
            #g2.add_edge(f, to, weight=edata['followers'])
            g2.add_edge(f,to)
    return g2

def write_json(gIn, fname):
	d3data = json_graph.node_link_data(gIn)
	with open(fname,'w') as outf:
		json.dump(d3data,outf)

#writes pajek - insert space int node name for quotes
def write_pajek(gIn, fname):
	with open(fname, 'w') as outf:
		net.write_pajek(gIn, outf) 

#for undirected graphs only
def print_dendogram(gIn):
	dendo = comm.generate_dendogram(gIn)
	for level in range(len(dendo) - 1):
		print "partition at level", level + "is",comm.partition_at_level(dendo,level)

fname = "/Users/arvind/Documents/College_2015/socialmedia_power/code/Infomap/infomap_output/acm_pajek1.map"
proc_g = ifmap._load_infomap(fname)

nodeset = [n for n in proc_g.nodes_iter()]
pos = net.graphviz_layout(proc_g, prog='neato')
net.draw_networkx_nodes(proc_g, pos, nodelist=nodeset, nodesize=50, node_color='blue', alpha=0.6)
net.draw_networkx_edges(proc_g, pos, width=0.5, alpha=0.5)

# print 'un-trimmed graph: ', len(o)
# core = trim_degrees(o, degree=2)
# print 'core after node pruning: ', len(core)
# core = trim_edges(core, weight=5)
# print 'core after edge pruning: ', len(core)
