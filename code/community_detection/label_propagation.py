from collections import Counter
import random

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

#sample usage
# labels = assign_labels(core)
# print labels
# print propagate_labels(core,labels)