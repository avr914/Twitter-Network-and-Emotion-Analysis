import networkx as net
import csv
import random
import os
import matplotlib.pyplot as plt

from collections import defaultdict
from collections import Counter
import math

## || RUN IN IPYTHON NOTEBOOK ||

twitter_network = []

with open('twitter-network_pgfo.csv') as f_datin:
    reader = csv.reader(f_datin,dialect='excel')
    twitter_network = [row for row in reader]

#twitter_network = [ line.strip().split('\t') for line in file('twitter_network.csv') ]

o = net.DiGraph()
hfollowers = defaultdict(lambda: 0)
for (twitter_user, followed_by, followers) in twitter_network:
    o.add_edge(twitter_user, followed_by, followers=int(followers))
    hfollowers[twitter_user] = int(followers)

SEED = 'avbytes'

# centre around the SEED node and set radius of graph
g = net.DiGraph(net.ego_graph(o, SEED, radius=4))

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

"""
for n in core.nodes():
    print n + " : " + str(core.neighbors(n))
    if len(core.neighbors(n)) < 1:
        core.remove_node(n)
        print "Removed " + n
"""


def assign_labels(gIn):
    i = 1
    labels = {}
    for n in gIn.nodes():
        labels[n] = i
        i += 1

    return labels

def choose_label(lst):
    if len(lst) == 1:
        return lst[0]
    data = Counter(lst).most_common()
    high = data[0][1]
    tmp = []
    for ele in data:
        if ele[1] < high:
            return random.choice(tmp)
        tmp.append(ele[0])
    return random.choice(tmp)

def propagate_labels(gIn,labels):
    node_list = labels.keys()
    for time in xrange(6):
        random.shuffle(node_list)
        for node in node_list:
            lst = [labels[n] for n in gIn.neighbors(node)]
            if len(lst) > 0:
                labels[node] = choose_label(lst)
            else:
                print node + " : " + str(lst)

    print "Stopped at time=" + str(time+1)
    return labels

# labels = assign_labels(core)
# print labels
# print propagate_labels(core,labels)
#start code - need to comment out
"""
nodeset_types = { 'TED': lambda s: s.lower().startswith('ted'), 'Not TED': lambda s: not s.lower().startswith('ted') }
"""
#start code - need to comment out
"""
nodesets = defaultdict(list)
"""

#start code - need to comment out
"""
for nodeset_typename, nodeset_test in nodeset_types.iteritems():
    nodesets[nodeset_typename] = [ n for n in core.nodes_iter() if nodeset_test(n) ]
"""

#my code
nodeset = [ n for n in core.nodes_iter() ]


pos = net.spring_layout(core) # compute layout

plt.figure(figsize=(18,18))
plt.axis('off')

colours = ['red','green']
colourmap = {}

# draw nodes
#start code - need to comment out

"""
i = 0
alphas = {'TED': 0.6, 'Not TED': 0.4}
for k in nodesets.keys():
    ns = [ math.log10(hfollowers[n]+1) * 80 for n in nodesets[k] ]
    print k, len(ns)
    net.draw_networkx_nodes(core, pos, nodelist=nodesets[k], node_size=ns, node_color=colours[i], alpha=alphas[k])
    colourmap[k] = colours[i]
    i += 1
print 'colourmap: ', colourmap
"""

#my code
colour = 'blue'
ns = [ math.log10(hfollowers[n]+1) * 80 for n in nodeset]
print len(ns)
net.draw_networkx_nodes(core, pos, nodelist=nodeset, nodesize=ns, node_color='blue', alpha=0.6)


# draw edges
net.draw_networkx_edges(core, pos, width=0.5, alpha=0.5)

#start code - need to comment out
# draw labels
"""
alphas = { 'TED': 1.0, 'Not TED': 0.5}
for k in nodesets.keys():
    for n in nodesets[k]:
        x, y = pos[n]
        plt.text(x, y+0.02, s=n, alpha=alphas[k], horizontalalignment='center', fontsize=9)
"""
#my code
for n in nodeset:
    x, y = pos[n]
    plt.text(x, y+0.02, s=n, alpha=1.0, horizontalalignment='center', fontsize=9)