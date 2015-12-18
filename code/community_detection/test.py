from collections import Counter
import random

lst = [1,2,1,3,4,5,6,7,3,2,5,1,4,3]

labels = [['a',1],['b',2],['c',3]]
random.shuffle(labels)
labels_dict = {x[0]:x[1] for x in labels}
print labels_dict
def choose_label(lst):
    if len(lst) == 1:
        return lst[0]
    data = Counter(lst).most_common()
    print data
    high = data[0][1]
    tmp = []
    for ele in data:
        if ele[1] < high:
            return random.choice(tmp)
        tmp.append(ele[0])
    return random.choice(tmp)

print choose_label(lst)

