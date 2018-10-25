
# coding: utf-8

# In[6]:


import sys, fileinput
from collections import defaultdict
import tree
#from __future__ import division


# In[8]:
freqs = defaultdict(int)
condCounts = defaultdict(int)
rule_count = 0
for line in fileinput.input():
    t = tree.Tree.from_str(line)
    prods = t.get_product()
    
    #prods = t.testing()
    #print prods
    for (x,y) in prods:
        freqs[(x,y)] += 1
        condCounts[x] += 1
max_value =  max(freqs.values())  
max_keys = [k for k, v in freqs.items() if v == max_value]
#print(max_value, max_keys)
for (x,y), freq in freqs.iteritems():
    rule_count +=1
    p = freq*1.0 / condCounts[x]
    print "%s -> %s # %.9f" % (x,y,p)
#(a,b)=(max_value, max_keys)
#print "number of  rules: %d" %rule_count
#print "The most frequent rule:"
#print max_keys
#print "Number of occurrence: %d" %max_value
#print(max_value, max_keys)
# In[1]:



# In[ ]:




