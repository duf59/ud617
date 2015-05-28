#!/usr/bin/python

import sys
import operator

# Loop around the data
# It will be in the format key\tval1\tval2
# key is the node_id, value1 is the node_type (question or answer) and value2 the body length
#
# for each key, we want to compute the question length and average answer length

oldKey = None
question_length = 0
answer_length = 0
count = 0

print "Question Node ID | \tQuestion Length | \tAverage Answer Length"


for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 3:
        # Something has gone wrong
        continue

    thisKey, thisType, thisLength = data_mapped

    if oldKey and oldKey != thisKey:
        if count>0: answer_length /= count # compute the mean
        print "{0}\t{1}\t{2}".format(oldKey, question_length, answer_length)
            
        oldKey = thisKey;
        question_length = 0
        answer_length = 0
        count = 0

    oldKey = thisKey
    if thisType=="question":
        question_length = thisLength
    elif thisType=="answer":
        answer_length += float(thisLength)
        count += 1

if oldKey != None:
    if count>0: answer_length /= count # compute the mean
    print "{0}\t{1}\t{2}".format(oldKey, question_length, answer_length)

