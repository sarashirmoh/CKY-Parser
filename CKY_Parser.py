from __future__ import division
import sys, fileinput
from collections import defaultdict
import math
#import time
#import matplotlib.pyplot as plt
#from sklearn import linear_model
#import numpy as np
import re
import itertools
from tree import Node


class Parser:
    def __init__(self, sent):
        self.p_list = defaultdict(float)      
        self.so_far = defaultdict(float)
        self.sent = sent.split()       
        self.unks = list(self.sent)  
        self.length = len(self.sent)
        self.rules = set()            
        self.track = {}           
        self.terminal = {} 
        self.nonterminal = set()
        
        #unk_tree = open(sys.argv[0])
        words = []
           
        #w_list = [ll.strip() for ll in unk_tree.readlines()]
        for l in fileinput.input():
            s = l.split()
            words += s
            
        for i,word in enumerate(self.sent):
            if any (word in su for su in words):
                pass
            else:
                self.sent[i] = "<unk>"        
        """if len(sys.argv) >= 3:
            unk_tree = open(sys.argv[2])
            words = []
           
            w_list = [ll.strip() for ll in unk_tree.readlines()]
            for l in w_list:
                s = l.split()
                words += s
            
            for i,word in enumerate(self.sent):
                if any (word in su for su in words):
                    pass
                else:
                    self.sent[i] = "<unk>"
                    if word.endswith("ing"):
                        self.sent[i] = "<unk-ing>"
                    elif word.endswith("s"):
                        self.sent[i] = "<unk-s>"
                    elif word.endswith("ed"):
                        self.sent[i] = "<unk-ed>"
                    elif word[0].isupper():
                        self.sent[i] = "<unk-Upper>"
                    elif len(word) == 1:
                        self.sent[i] = "<unk-letter>"
                   
                    elif not word[0].isalpha():
                        self.sent[i] = "<unk-'>"
                    else:
      
                        self.sent[i] = "<unk>" """
                
           
    def backtrack(self, (st,en,label)):
                       
        if (st,en,label) not in self.track:
            if (st,en,label) in self.terminal:
                N = Node(label = label, terminal_w = self.unks[st], children = [])
            return N
        sub_tree = self.track[(st,en,label)]

        if len((st,en,label)) == 3:
            (split, left, right) = sub_tree
       
            sub_tree_1 = self.backtrack((st, split, left))     
            sub_tree_2 = self.backtrack((split, en, right)) 
            N = Node(label = label, children = [sub_tree_1,sub_tree_2])
            return N
        
        if len(sub_tree) == 1:
            sub_tree_1 = self.backtrack((st,en,sub_tree[0]))
            N = Node(label = sub_tree[0], children = [sub_tree_1])
            return N    

    def U_calc(self,start, end):
        
        for i in self.nonterminal:
            for j in self.nonterminal:
                if (i,j) in self.rules:
                    new_p = self.p_list[(i,j)] * self.so_far[(start,end,j)]
        
                    if new_p > self.so_far[(start,end,i)]:
                        self.so_far[(start, end, i)] = new_p
                        self.track[(start, end, i)] = (j,)    
    
    def CKY(self):
       
        #grammar_file = open(sys.argv[0])
        total_score = 0
        node_list = None
        for rule in fileinput.input():
            g_rule = re.split(r"\-\>|\#", rule.strip())
            NN = g_rule[0]
            
            PP = g_rule[1]
            p = float(g_rule[2].strip())
            NN = NN.strip()
            PP = PP.strip()
            
            self.nonterminal.add(NN)
            self.rules.add( (NN,PP) )
            self.p_list[(NN,PP)] = p
         
        for pos in range(0,self.length):
            for nnode in self.nonterminal:
                if self.sent[pos] == "'s":
                    self.sent[pos] = "is"
                if (nnode,self.sent[pos]) in self.rules:
                    self.terminal[(pos,pos+1,nnode)] = self.sent[pos]
                    self.so_far[(pos,pos+1,nnode)] = self.p_list[(nnode, self.sent[pos])]
            self.U_calc(pos,pos+1)
        for r in range(2,self.length+1):
            for start in range(0,self.length-r+1):
                for split in range(start+1,start + r):
                    for y,z in self.rules:
                        if len(z.split()) == 2:
                            (child_1, child_2) = (z.split()[0].strip(),z.split()[1].strip())
                            new_p = self.p_list[(y, z)] * self.so_far[(start,split,child_1)] * self.so_far[(split, start + r, child_2)]
                            if cmp(new_p ,self.so_far[(start, start + r,  y)]) > 0:
                                self.so_far[(start, start + r, y)] = new_p
                                self.track[(start, start + r, y)] = (split, child_1, child_2)
                self.U_calc(start,start + r)
        if (0,len(self.sent),'TOP') in self.track:
             node_list = self.backtrack((0,len(self.sent),'TOP'))
  
        if node_list is not None:
            my_list = []    
            ddd = node_list.print_parser_2(my_list)
            print "".join(str(x) for x in ddd)

        else:
            print 

if __name__ == "__main__":

    for line in sys.stdin:
        #ttt = tree.Tree.from_str(line)
        s = Parser(line.strip())
        s.CKY()    
    """x_values = []
    y_values = []
    counter_lines  = 0
    for line in sys.stdin:
        tic = time.clock()
        #ttt = tree.Tree.from_str(line)
        s = Parser(line.strip())
        s.CKY()
        toc = time.clock()
        y_values.append(toc - tic)
        x_values.append(len(line.split()))
        counter_lines += 1
    
    plt.loglog(x_values, y_values, basex=10, basey=10, linestyle='None', marker='x', markeredgecolor='red')
    plt.show()
    
    result_x = map(lambda x: x * 1.0, x_values)
    reg = linear_model.LinearRegression()
    
    x = np.array(map(lambda x: math.log10(x),result_x))
    y = np.array(map(lambda x: math.log10(x),y_values))
    reg.fit(x.reshape(counter_lines,1), y)
    print reg.coef_"""
    
    





