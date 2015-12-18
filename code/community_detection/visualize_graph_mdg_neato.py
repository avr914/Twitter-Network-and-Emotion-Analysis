import networkx as net
from networkx.readwrite import json_graph
import csv
import os
import json
import matplotlib.pyplot as plt
import pygraphviz as pgv
import sys

from collections import defaultdict
import math

## || RUN IN IPYTHON NOTEBOOK ||

twitter_network = []

with open('acm_edges1.csv') as f_datin:
    reader = csv.reader(f_datin,dialect='excel')
    twitter_network = [row for row in reader]

#twitter_network = [ line.strip().split('\t') for line in file('twitter_network.csv') ]

o = net.MultiDiGraph()
hfollowers = defaultdict(lambda: 0)
for (twitter_user, followed_by, followers) in twitter_network:
    #o.add_edge(twitter_user, followed_by)
    name_user = "U: " + twitter_user
    name_follower = name = "U: " + followed_by
    o.add_edge(name_user, name_follower, followers=int(followers))
    hfollowers[name_user] = int(followers)

SEED = 'acmuiuc'

# centre around the SEED node and set radius of graph
g = net.MultiDiGraph(o)

# set of seed's followers
# fname = os.path.join('avbytes_following',SEED + '.csv')
# direct_friends = set()
# with open(fname) as f_seeddat:
#     reader = csv.reader(f_seeddat, dialect='excel')
#     direct_friends = set(row[1] for row in reader)

# direct_friends.add(SEED)
#print direct_friends

def trim_degrees(gIn, degree=1):
    g2 = gIn.copy()
    d = net.degree(g2)
    for n in g2.nodes():
        if n == SEED: continue # don't prune the SEED node
        if d[n] <= degree:
            g2.remove_node(n)
    return g2

# def trim_edges_new(gIn, weight=1):
#     g2 = net.MultiDiGraph()
#     for n,nbrsdict in g.adjacency_iter():
#         for nbr,keydict in nbrsdict.items():
#             for key,eattr in keydict.items():
#                 if n == SEED or nbr == SEED:
#                     g2.add_edge(n,nbr,weight=eattr['followers']) 
#                 elif eattr['followers'] >= weight:
#                     g2.add_edge(n,nbr,weight=eattr['followers'])
#     return g2  

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

print 'g: ', len(g)
core = trim_degrees(g, degree=2)
#core = trim_degrees_post(g, degree=2)
print 'core after node pruning: ', len(core)
core = trim_edges(core, weight=5)
print 'core after edge pruning: ', len(core)

#writes networkx graph to json file for external visualization ie. D3
d3data = json_graph.node_link_data(core)

with open('testdata.json','w') as outf:
    json.dump(d3data,outf)

#writes networkx graph to pajek file for infomap analysis
pajek_outf = os.path.join('/Users/arvind/Documents/College_2015/socialmedia_power/code','acm_pajek1.net')
with open(pajek_outf, 'w') as outf:
    net.write_pajek(core, outf)

sys.exit()

#my code
nodeset = [ n for n in core.nodes_iter() ]
#nodeset.remove(SEED)

pos = net.graphviz_layout(core, prog='neato') # compute alyout

plt.figure(figsize=(30,30))
plt.axis('off')

colours = ['red','green']
colourmap = {}

#my code
colour = 'blue'
ns = [ math.log10(hfollowers[n]+1) * 80 for n in nodeset]
print len(ns)
#net.draw_networkx_nodes(core,pos, nodelist=[SEED], nodesize=500,node_color='red',alpha=0.8)
net.draw_networkx_nodes(core, pos, nodelist=nodeset, nodesize=ns, node_color='blue', alpha=0.6)

# draw edges
net.draw_networkx_edges(core, pos, width=0.5, alpha=0.5)

#my code
i = 0
for n in nodeset:
    x, y = pos[n]
    plt.text(x, y, s=i, alpha=1.0, horizontalalignment='center', fontsize=9)
    i += 1