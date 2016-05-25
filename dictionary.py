#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import re

f1 = open("terms_txt/wiki_terms.txt", "r", encoding='utf-8')
f2 = open("terms_txt/doosan_terms.txt", "r", encoding="utf-8")
f3 = open("terms_txt/wiki_labels.txt", "r", encoding="utf-8")
p1 = open("dict/wiki_terms.pickle","wb")
p2 = open("dict/doosan_terms.pickle","wb")

wiki_terms = {}
for line in f1.readlines() :

    line = line.replace("\n","")
    if "(" in line:
        index = line.index("(")-1
    else:
        index = len(line)

    wiki_terms[line.replace("_", "")[:index].replace("(","")] = 0

for line in f3.readlines() :
    term = line.split("\t")

    if "틀:" in term[0] :
        term[0] = term[0].replace("틀:","")
    if "분류:" in term[0]:
        term[0] = term[0].replace("분류:", "")
    if "(동음이의)" in term[0] :
        term[0] = term[0].replace("(동음이의)","")
    term[0] = term[0].replace(" ", "")


    if "(" in term[0] :
        try :
            category = term[0][term[0].index("(")+1:term[0].index(")")]
            term[1] = term[1].replace("\n","")
            term[1] += "|"+category
            term[0] = term[0][:term[0].index("(")]
        except :
            continue

    term[0] = re.sub('\(\w*\)', '', term[0])

    wiki_terms[term[0]] = term[1]

pickle.dump(wiki_terms, p1)

doosan_terms = {}
for line in f2.readlines() :\

    tokens = line.split("\t")
    if "(" in tokens[0] :
        index = tokens[0].index("(") - 1
    else :
        index = len(tokens[0])

    doosan_terms[tokens[0][:index].replace("(","").replace(" ", "")] = tokens[1]

pickle.dump(doosan_terms, p2)