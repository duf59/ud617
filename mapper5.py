#!/usr/bin/python
import sys
import csv
import re

# Input is a text file
#
# Key is the request, value is the node_id
# We write them out to standard output, separated by a tab

reader = csv.reader(sys.stdin, delimiter='\t')
writer = csv.writer(sys.stdout, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

for line in reader:
    node_id = line[0]
    if re.match(r'^\d*$',node_id):
        words = line[4].lower().strip()
        words = re.split(r'\W+',words)
        for word in words:
            if word != "":
                print "{0}\t{1}".format(word, node_id)


