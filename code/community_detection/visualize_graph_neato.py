import networkx as net
import csv
import os
import matplotlib.pyplot as plt
import pygraphviz as pgv

from collections import defaultdict
import math

## || RUN IN IPYTHON NOTEBOOK ||

twitter_network = []

with open('twitter-network_pgfo.csv') as f_datin:
    reader = csv.reader(f_datin,dialect='excel')
    twitter_network = [row for row in reader]

#twitter_network = [ line.strip().split('\t') for line in file('twitter_network.csv') ]

o = net.MultiDiGraph()
hfollowers = defaultdict(lambda: 0)
for (twitter_user, followed_by, followers) in twitter_network:
    o.add_edge(twitter_user, followed_by, followers=int(followers))
    hfollowers[twitter_user] = int(followers)

SEED = 'avbytes'

# centre around the SEED node and set radius of graph
g = net.MultiDiGraph(net.ego_graph(o, SEED, radius=4))

# set of seed's followers
fname = os.path.join('avbytes_following',SEED + '.csv')
direct_friends = set()
with open(fname) as f_seeddat:
    reader = csv.reader(f_seeddat, dialect='excel')
    direct_friends = set(row[1] for row in reader)

direct_friends.add(SEED)
#print direct_friends

def trim_degrees(gIn, degree=1):
    g2 = gIn.copy()
    d = net.degree(g2)
    for n in g2.nodes():
        if n == SEED: continue # don't prune the SEED node
        if d[n] <= degree:
            g2.remove_node(n)
    return g2

def trim_degrees_post(gIn, degree=1):
    g2 = gIn.copy()
    file = open('df_count_log.log','w+')
    for n in g2.nodes():
        neighbors = g2.neighbors(n)
        df_count = 0
        for neighbor in neighbors:
            if neighbor in direct_friends:
                df_count += 1
                file.write(n + " : " + str(df_count) + "\n")

        if df_count < degree:
            g2.remove_node(n)

    return g2

def trim_edges(gIn, weight=1):
    g2 = net.DiGraph()
    for f, to, edata in gIn.edges_iter(data=True):
        if f == SEED or to == SEED: # keep edges that link to the SEED node
            g2.add_edge(f, to, edata)
        elif edata['followers'] >= weight:
            g2.add_edge(f, to, edata)
    return g2 

print 'g: ', len(g)
core = trim_degrees(g, degree=2)
#core = trim_degrees_post(g, degree=2)
print 'core after node pruning: ', len(core)
core = trim_edges(core, weight=5)
print 'core after edge pruning: ', len(core)
core = g

#my code
nodeset = [ n for n in core.nodes_iter() ]
nodeset.remove(SEED)

pos = net.graphviz_layout(core, prog='neato') # compute alyout

plt.figure(figsize=(18,18))
plt.axis('off')

colours = ['red','green']
colourmap = {}

#my code
colour = 'blue'
ns = [ math.log10(hfollowers[n]+1) * 80 for n in nodeset]
print len(ns)
net.draw_networkx_nodes(core,pos, nodelist=[SEED], nodesize=500,node_color='red',alpha=0.8)
net.draw_networkx_nodes(core, pos, nodelist=nodeset, nodesize=ns, node_color='blue', alpha=0.6)

# draw edges
net.draw_networkx_edges(core, pos, width=0.5, alpha=0.5)

#my code
i = 0
for n in nodeset:
    x, y = pos[n]
    plt.text(x, y, s=i, alpha=1.0, horizontalalignment='center', fontsize=9)
    i += 1