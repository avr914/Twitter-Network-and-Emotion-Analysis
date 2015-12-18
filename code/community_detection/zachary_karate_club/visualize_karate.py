import networkx as net
import os
import random
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import pygraphviz as pgv

src_file = os.path.join('karate_src_files','karate.gml')
graph = net.read_gml(src_file)

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
    for time in xrange(10):
        random.shuffle(node_list)
        for node in node_list:
            lst = [labels[n] for n in gIn.neighbors(node)]
            if len(lst) > 0:
                labels[node] = choose_label(lst)
            else:
                print node + " : " + str(lst)

    print "Stopped at time=" + str(time+1)
    return labels

labels = assign_labels(graph)
print labels
result = propagate_labels(graph,labels)
print result

label_counter = defaultdict(lambda : [])
for user,label in result.iteritems():
    label_counter[label].append(user) 

for label,usr_lst in label_counter.iteritems():
    print str(label) + " : " + str(usr_lst)

#matplotlib graph-drawing code
nodeset = [ n for n in graph.nodes_iter() ]

#nodesets
nodesets = label_counter

#pos = net.spring_layout(graph,iterations=50) # compute layout
pos = net.graphviz_layout(graph, prog='neato') 

plt.figure(figsize=(18,18))
plt.axis('off')

colours = ['red','green','blue','gray','yellow','orange']
tmp_list = []
tmp_string = 'abcdefghijklmnopqrstuvwxyz'
tmp_string = ''.join(random.sample(tmp_string,len(tmp_string)))
for i in xrange(8):
    tmp_list.append(tmp_string[i])
    
colours.extend(tmp_list)
colourmap = {}

i = 0
for n in nodesets.iterkeys():
    net.draw_networkx_nodes(graph, pos, nodelist=nodesets[n],node_size=450, node_color=colours[i], alpha=0.6)    
    colourmap[n] = colours[i]
    i += 1

print 'colourmap: ' + str(colourmap)
#net.draw_networkx_nodes(graph, pos, nodelist=nodeset,node_size=450, node_color='grey', alpha=0.6)
net.draw_networkx_edges(graph, pos, width=0.5, alpha=0.8)

for n in nodeset:
    x, y = pos[n]
    plt.text(x, y, s=n, alpha=1.0, horizontalalignment='center', fontsize=10,style='oblique')