#!/usr/bin/python

import sys
import operator

# Loop around the data
# It will be in the format key\tval
# key is the author_id, value is the hour at which message was posted
#
# for each key, we want to find the most occurent hour
# to do this we store the count of each hour in a dictionnary, and sort it
# (if there are ties, we keep them all)

oldKey = None
dicHour = {}

print "Student ID | \tHour"

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong
        continue

    thisKey, thisHour = data_mapped

    if oldKey and oldKey != thisKey:
        # sort and print out
        sorted_hours = sorted(dicHour.items(), key = operator.itemgetter(1), reverse = True)
        topCount = sorted_hours[0][1]
        for tuple in sorted_hours:
            if tuple[1]==topCount: print "{0}\t{1}".format(oldKey,tuple[0])
            
        oldKey = thisKey;
        dicHour = {}

    oldKey = thisKey
    # update dictionnary
    if thisHour in dicHour:
        dicHour[thisHour] += 1
    else:
        dicHour[thisHour] = 1

if oldKey != None:
    # sort and print out (last key)
    sorted_hours = sorted(dicHour.items(), key = operator.itemgetter(1), reverse = True)
    topCount = sorted_hours[0][1]
    for tuple in sorted_hours:
        if tuple[1]==topCount: print "{0}\t{1}".format(oldKey,tuple[0])

