#!/usr/bin/python

import sys
import operator

# Loop around the data
# It will be in the format key\tval
# key is forum thread id, value is the author id
#
# we want to find all authors taking part in a thread
# to do this we store the author ids in a list and print it

oldKey = None
author_list = []

print "Tag\tCounts"

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong
        continue

    thisKey, thisAuthor = data_mapped

    if oldKey and oldKey != thisKey:
        print "{0}\t{1}".format(oldKey,author_list)
        oldKey = thisKey;
        author_list = []

    oldKey = thisKey
    author_list.append(int(thisAuthor))

if oldKey != None:
    print "{0}\t{1}".format(oldKey,author_list)

