#!/usr/bin/python
import sys
import csv
import re
from datetime import datetime

# Input is a text file (tab delimited, fields enclosed in doublequotes)
#
# Key is the request, value is the node_id
# We write them out to standard output, separated by a tab

reader = csv.reader(sys.stdin, delimiter='\t')
reader.next()
for line in reader:

    # parse
    node_id, title, tagnames, author_id, body, node_type, parent_id, abs_parent_id,\
    added_at, score, state_string, last_edited_id, last_activity_by_id, last_activity_at,\
    active_revision_id,	extra, extra_ref_id, extra_count, marked = line

    hour = datetime.strptime(added_at.split(".")[0], "%Y-%m-%d %H:%M:%S").hour

    # for debug:
    '''
    print "\nNew entry -------------------------------------------------\n\n"
    print "id\t{0}".format(node_id)
    print "title\t{0}".format(title)
    print "tagnames\t{0}".format(tagnames)
    print "author_id\t{0}".format(author_id)
    print "body\t{0}".format(body)
    print "node_type\t{0}".format(node_type)
    print "parent_id\t{0}".format(parent_id)
    print "abs_parent_id\t{0}".format(abs_parent_id)
    print "added_at\t{0}".format(added_at)
    print "hour\t{0}".format(hour)
    '''

    print "{0}\t{1}".format(author_id, hour)





