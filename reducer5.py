#!/usr/bin/python

import sys

# Loop around the data
# It will be in the format key\tval
# Where key is the word, val is the node_id
#
# for each key, we put all the node_id into a list

oldWord = None
NodeList = []

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong. Skip this line.
        continue

    thisWord, thisNode = data_mapped

    if oldWord and oldWord != thisWord:
        print oldWord, "\t", NodeList
        oldWord = thisWord;
        NodeList = []

    oldWord = thisWord
    NodeList.append(int(thisNode))

if oldWord != None:
    print oldWord, "\t", NodeList

