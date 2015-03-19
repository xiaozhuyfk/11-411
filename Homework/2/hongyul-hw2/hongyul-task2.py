# hw2
# hongyul-task2.py
# Hongyu Li

import os, sys, re

################################################################################
#  Read & Write functions from 112 webpage
################################################################################

# Read a file
# filename is the path of the file, string type
# returns the content as a string
def readFile(filename, mode="rt"):
    # rt stands for "read text"
    fin = contents = None
    try:
        fin = open(filename, mode)
        contents = fin.read()
    finally:
        if (fin != None): fin.close()
    return contents

# Write 'contents' to the file
# 'filename' is the path of the file, string type
# 'contents' is of string type
# returns True if the content has been written successfully
def writeFile(filename, contents, mode="wt"):
    # wt stands for "write text"
    fout = None
    try:
        fout = open(filename, mode)
        fout.write(contents)
    finally:
        if (fout != None): fout.close()
    return True


################################################################################
#   Task 2
################################################################################

# Globals
dictionary = {}
dict_spec = {}
dict_1 = {}
dict_2 = {}
dict_3 = {}
dict_4 = {}
dict_5 = {}
sample = {}
sample_spec = {}
sample_1 = {}
sample_2 = {}
sample_3 = {}
sample_4 = {}
sample_5 = {}
mapping = {}

src_dir = "nyt"
encoded = "mit.txt"
decoded = "hongyul-task2.txt"



# Init frequency analysis
def init():
    print "Initializing ..."
    files = os.listdir(src_dir)
    for filename in files:
        path = src_dir + "/" + filename
        content = readFile(path)

        words = re.split("(\W+)", content)
        for i in xrange(len(words)):
            word = words[i].lower()
            if (word.isalpha()):
                if (word in dictionary):
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1
            elif (word == "'"):
                if (i+1 < len(words) and
                    words[i+1].isalpha()):
                    token = word + words[i+1]
                    if (token in dict_spec):
                        dict_spec[token] += 1
                    else:
                        dict_spec[token] = 1

    for word in dictionary:
        if (len(word) == 1):
            dict_1[word] = dictionary[word]
        elif (len(word) == 2):
            dict_2[word] = dictionary[word]
        elif (len(word) == 3):
            dict_3[word] = dictionary[word]
        elif (len(word) == 4):
            dict_4[word] = dictionary[word]
        elif (len(word) == 5):
            dict_5[word] = dictionary[word]

    msg = readFile(encoded)
    words = re.split("(\W+)", msg)
    for i in xrange(len(words)):
        word = words[i].lower()
        if (word.isalpha()):
            if (word in sample):
                sample[word] += 1
            else:
                sample[word] = 1
        elif (word == "'"):
            if (i+1 < len(words) and words[i+1].isalpha()):
                token = word + words[i+1]
                if (token in sample_spec):
                    sample_spec[token] += 1
                else:
                    sample_spec[token] = 1
    for word in sample:
        if (len(word) == 1):
            sample_1[word] = sample[word]
        elif (len(word) == 2):
            sample_2[word] = sample[word]
        elif (len(word) == 3):
            sample_3[word] = sample[word]
        elif (len(word) == 4):
            sample_4[word] = sample[word]
        elif (len(word) == 5):
            sample_5[word] = sample[word]

    print "Initialization complete."

def get_rank(dic):
    return sorted(dic.items(), key = lambda d: d[1])[::-1]

def make_mapping(d, s):
    for i in xrange(len(d)):
        word = d[i][0]
        enigma = s[i][0]
        for j in xrange(len(word)):
            if (enigma[j] not in mapping):
                mapping[enigma[j]] = word[j]
        
        

def match():
    dict_rank = get_rank(dictionary)
    sample_rank = get_rank(sample)
    dict1_rank = get_rank(dict_1)
    dict2_rank = get_rank(dict_2)
    dict3_rank = get_rank(dict_3)
    dict4_rank = get_rank(dict_4)
    dict5_rank = get_rank(dict_5)
    sample1_rank = get_rank(sample_1)
    sample2_rank = get_rank(sample_2)
    sample3_rank = get_rank(sample_3)
    sample4_rank = get_rank(sample_4)
    sample5_rank = get_rank(sample_5)

    # first manual adjustment
    # After the first round, some words are already pretty recognizable,
    # like "who" "has" "been" "dean" "admission", so I manually changed
    # the following characters
    mapping['f'] = 'w'
    mapping['i'] = 'h'
    mapping['m'] = 'f'
    mapping['v'] = 'a'
    mapping['y'] = 'b'
    mapping['e'] = 'c'
    mapping['r'] = 'm'

    # second manual adjustment
    # This round of manual adjustment, I recognize some words such as
    # appointments, announce
    mapping['a'] = 'v'
    mapping['b'] = 'y'
    mapping['d'] = 'k'
    mapping['l'] = 'p'
    mapping['w'] = 'u'
    mapping['x'] = 'g'
    mapping['z'] = 'l'

    # third manual adjustment
    # Words like emphasizes, January help me complete the final adjustment
    mapping['h'] = 'j'
    mapping['q'] = 'x'
    mapping['g'] = 'z'
    mapping['u'] = 'q'

    
    make_mapping(dict2_rank[:4], sample2_rank[:8])
    make_mapping(dict3_rank[:4], sample3_rank[:8])
    make_mapping(dict4_rank[:4], sample4_rank[:8])
    make_mapping(dict5_rank[:4], sample5_rank[:8])
    make_mapping(dict1_rank[:4], sample1_rank[:8])
    
    make_mapping(dict2_rank[3:20], sample2_rank[3:20])
    make_mapping(dict3_rank[3:20], sample3_rank[3:20])
    make_mapping(dict4_rank[3:20], sample4_rank[3:20])
    make_mapping(dict5_rank[3:20], sample5_rank[3:20])
    make_mapping(dict1_rank[3:8], sample1_rank[3:8])

    capital = {}
    for c in mapping:
        n = c.upper()
        capital[n] = mapping[c].upper()
    mapping.update(capital)
    
    print mapping, len(mapping), len(sample1_rank)

    
def decode():
    rep = dict((re.escape(k), v) for k, v in mapping.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    content = pattern.sub(lambda m: rep[re.escape(m.group(0))], "abcdefghijklmn");
    print content
    
    content = readFile(encoded)
    content = pattern.sub(lambda m: rep[re.escape(m.group(0))], content);
    writeFile(decoded, content)


def main():
    init()
    match()
    decode()

main()
                    
