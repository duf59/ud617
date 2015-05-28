# Some MapReduce Codes to analyze forum threads

We work with discussion forum / discussion board data.
The dataset is taken from Udacity forums. Udacity forums are run on free, opensource software called OSQA, which was designed to be similar to StackOverflow forums. The basic structure is - the forum has nodes. All nodes have a body and author_id. Top level nodes are called questions, and will also have a title and tags. Questions can have answers. Both questions and answers can have comments.

## dataset

Datasets are not included in this repo (too large). They can be obtained from the class "Intro to Hadoop and MapReduce" on udacity ("forum_data").

There are 2 files in the dataset. The first is "forum_nodes.tsv", it contains all forum questions and answers in one table. It was exported from the RDBMS by using tab as a separator, and enclosing all fields in doublequotes. 
Field names are indicated in the first line of the file "forum_node.tsv".
The ones that are the most relevant here are:

* "id": id of the node
* "title": title of the node. in case "node_type" is "answer" or "comment", this field will be empty
* "tagnames": space separated list of tags
* "author_id": id of the author
* "body": content of the post
* "node_type": type of the node, either "question", "answer" or "comment"
* "parent_id": node under which the post is located, will be empty for "questions"
* "abs_parent_id": top node where the post is located
* "added_at": date added

The second table is "forum_users.tsv". It contains fields for "user_ptr_id" - the id of the user. "reputation" - the reputation, or karma of the user, earned when other users upvote their posts, and the number of "gold", "silver" and "bronze" badges earned.

In the following we show some simple MapReduce codes, writen in python, aiming at analyzing this dataset on a Hadoop Cluster (A virtual machine with a Coloudera Hadoop Distribution was used).

## Students and Posting Time on Forums

We want to know for each student what is the hour during which the student has posted the most posts
(we ignore the time-zone offset). --> see mapper1.py and reducer1.py (or codes below)

mapper : 
```
#!/usr/bin/python
import sys
import csv
from datetime import datetime

reader = csv.reader(sys.stdin, delimiter='\t')
reader.next() # skip first line containing headers (for local use only)
for line in reader:
    # parse
    node_id, title, tagnames, author_id, body, node_type, parent_id, abs_parent_id,\
    added_at, score, state_string, last_edited_id, last_activity_by_id, last_activity_at,\
    active_revision_id,	extra, extra_ref_id, extra_count, marked = line

    hour = datetime.strptime(added_at.split(".")[0], "%Y-%m-%d %H:%M:%S").hour

    print "{0}\t{1}".format(author_id, hour)
```

reducer :
```
#!/usr/bin/python

import sys
import operator

oldKey = None
dicHour = {}

print "Student ID | \tHour"

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2: continue

    thisKey, thisHour = data_mapped

    if oldKey and oldKey != thisKey:
        sorted_hours = sorted(dicHour.items(), key = operator.itemgetter(1), reverse = True)
        topCount = sorted_hours[0][1]
        for tuple in sorted_hours:
            if tuple[1]==topCount: print "{0}\t{1}".format(oldKey,tuple[0])
            
        oldKey = thisKey;
        dicHour = {}

    oldKey = thisKey
    if thisHour in dicHour:
        dicHour[thisHour] += 1
    else:
        dicHour[thisHour] = 1

if oldKey != None:
    sorted_hours = sorted(dicHour.items(), key = operator.itemgetter(1), reverse = True)
    topCount = sorted_hours[0][1]
    for tuple in sorted_hours:
        if tuple[1]==topCount: print "{0}\t{1}".format(oldKey,tuple[0])
```

## Post and answer length

We are interested to see if there is a correlation between the length of a post and the length of answers.

Write a mapreduce program that would process the forum_node data and output the length of the post and the average answer (just answer, not comment) length for each post. You will have to decide how to write both the mapper and the reducer to get the required result. --> see mapper2.py and reducer2.py (or codes below)

mapper:
```
#!/usr/bin/python
import sys
import csv

reader = csv.reader(sys.stdin, delimiter='\t')
reader.next() # skip first line, for local use only
for line in reader:
    # parse
    node_id, title, tagnames, author_id, body, node_type, parent_id, abs_parent_id,\
    added_at, score, state_string, last_edited_id, last_activity_by_id, last_activity_at,\
    active_revision_id,	extra, extra_ref_id, extra_count, marked = line

    key = node_type
    if node_type=="question":
        print "{0}\t{1}\t{2}".format(node_id, node_type, len(body))
    elif node_type == "answer":
        print "{0}\t{1}\t{2}".format(parent_id, node_type, len(body))
```

reducer:
```
#!/usr/bin/python
import sys
import operator

oldKey = None
question_length = 0
answer_length = 0
count = 0

print "Question Node ID | \tQuestion Length | \tAverage Answer Length"

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 3: continue

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
```

## Top Tags

We are interested seeing what are the top tags used in posts.

The mapreduce program outputs Top 10 tags, ordered by the number of questions they appear in.
We only look at tags appearing in questions themselves (i.e. nodes with node_type "question"), not on answers or comments. --> see mapper3.py and reducer3.py or codes below (we could also add a combiner for more efficient computation).

mapper:
```
#!/usr/bin/python
import sys
import csv

reader = csv.reader(sys.stdin, delimiter='\t')
reader.next() # skip first line for local use only
for line in reader:
    # parse
    node_id, title, tagnames, author_id, body, node_type, parent_id, abs_parent_id,\
    added_at, score, state_string, last_edited_id, last_activity_by_id, last_activity_at,\
    active_revision_id,	extra, extra_ref_id, extra_count, marked = line

    if node_type=="question":
        for tag in tagnames.split():
            print "{0}\t{1}".format(tag, 1)
```

reducer:
```
#!/usr/bin/python
import sys
import operator

oldKey = None
dicTag = {}
count = 0

print "Tag\tCounts"

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2: continue

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
```

## Study Group

We want to help students form study groups. But first we want to see if there are already students on forums that communicate a lot between themselves.

As the first step for this analysis we write a mapreduce program that for each forum thread (that is a question node with all it's answers and comments) give us a list of students that have posted there - either asked the question, answered a question or added a comment. If a student posted to that thread several times, they are added to that list several times as well, to indicate intensity of communication. --> see mapper4.py and reducer4.py or codes below (we could use a combiner here too).

mapper:
```
#!/usr/bin/python
import sys
import csv

reader = csv.reader(sys.stdin, delimiter='\t')
reader.next() # skip first line for local use only
for line in reader:

    # parse
    node_id, title, tagnames, author_id, body, node_type, parent_id, abs_parent_id,\
    added_at, score, state_string, last_edited_id, last_activity_by_id, last_activity_at,\
    active_revision_id,	extra, extra_ref_id, extra_count, marked = line

    if node_type=="question":
        print "{0}\t{1}".format(node_id, author_id)
    elif node_type in ["answer","comment"]:
        print "{0}\t{1}".format(parent_id, author_id)
```

reducer:
```
#!/usr/bin/python
import sys
import operator

oldKey = None
author_list = []

print "Tag\tCounts"

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2: continue

    thisKey, thisAuthor = data_mapped

    if oldKey and oldKey != thisKey:
        print "{0}\t{1}".format(oldKey,author_list)
        oldKey = thisKey;
        author_list = []

    oldKey = thisKey
    author_list.append(int(thisAuthor))

if oldKey != None:
    print "{0}\t{1}".format(oldKey,author_list)
```

## Building an inverted Index

From the body of the forum posts we build an inverted index.
This is an index of all words that can be find in the body and node id they can be found in.
We split the text on all whitespaces as well as the following characters: .,!?:;"()<>[]#$=-/ (no html parsing)

Mapper and Reducer codes are in the Inverted_index/ folder, along with a testfile (original file is about 100mb).
Output is not included (too large). --> see mapper5.py and reducer5.py or codes below.

mapper:
```
#!/usr/bin/python
import sys
import csv
import re

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
```

reducer:
```
#!/usr/bin/python
import sys

oldWord = None
NodeList = []

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2: continue

    thisWord, thisNode = data_mapped

    if oldWord and oldWord != thisWord:
        print oldWord, "\t", NodeList
        oldWord = thisWord;
        NodeList = []

    oldWord = thisWord
    NodeList.append(int(thisNode))

if oldWord != None:
    print oldWord, "\t", NodeList
```


