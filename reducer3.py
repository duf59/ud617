#!/usr/bin/python

import sys
import operator

# Loop around the data
# It will be in the format key\tval
# key is thetag, value is 1
#
# we want to find the top 10 tags
# to do this we store the tags and corresponding count in a dictionnary, and sort it
# (if there are ties, we keep them all)

oldKey = None
dicTag = {}
count = 0

print "Tag\tCounts"

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong
        continue

    thisKey = data_mapped[0]

    if oldKey and oldKey != thisKey:
        dicTag[oldKey] = count
        oldKey = thisKey;
        count = 0

    oldKey = thisKey
    count += 1

if oldKey != None:
    dicTag[oldKey] = count

# sort and print
sorted_tags = sorted(dicTag.items(), key = operator.itemgetter(1), reverse = True)
for tuple in sorted_tags[0:10]:
    print "{0}\t{1}".format(tuple[0],tuple[1])
            

