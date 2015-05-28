#!/usr/bin/python

# Input is in Common Log Format
#
# Key is the IP
# Value is 1 (we just want to count the number of hits to the site made by each different IP)
# We write them out to standard output, separated by a tab

import sys
import re

for line in sys.stdin:
    data = line.strip().split()
    if len(data)>1:
        print "{0}\t{1}".format(data[0], 1)

