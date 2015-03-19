# hw3
# hongyul-hw3.py
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
#   Helper functions to calculate distance
################################################################################


# a trie node structure
class trie_node:
    def __init__(self, char, parent):
        self.word = None
        self.char = char
        self.parent = parent
        self.letters = {}

    def insert(self, word):
        node = self
        for c in word:
            if (c not in node.letters):
                node.letters[c] = trie_node(c, node)
            node = node.letters[c]
        node.word = word
        return node


# This is the version before using trie
"""
def memoized(f):
    import functools
    cachedResults = dict()
    @functools.wraps(f)
    def wrapper(*args):
        if args not in cachedResults:
            cachedResults[args] = f(*args)
        return cachedResults[args]
    return wrapper

@memoized
def D(w1, w2, i, j, m):
    if (i == 0 and j == 0):
        return (0, "")
    if (i < 0 or i > len(w1) or j < 0 or j > len(w2)):
        return (sys.maxint, "")
    
    Dins = D(w1, w2, i-1, j, m)
    if (Dins[0] != sys.maxint):
        Dins = (Dins[0] + 1, Dins[1])


    Ddel = D(w1, w2, i, j-1, m)
    if (Ddel[0] != sys.maxint):        
        Ddel = (Ddel[0] + 1, Ddel[1] + w2[j-1])
    
    Dsub = D(w1, w2, i-1, j-1, m)
    if (Dsub[0] != sys.maxint):
        Dsub = (Dsub[0] + (w1[i-1] != w2[j-1]), Dsub[1] + w2[j-1])

    Dtran = D(w1, w2, i-2, j-2, m)
    if (Dtran[0] != sys.maxint):
        if (w1[i-2] == w2[j-1] and w1[i-1] == w2[j-2]):
            Dtran = (Dtran[0] + 1, Dtran[1] + w1[i-1] + w2[j-1])
        else:
            Dtran = (sys.maxint, "")

    #print (min(Dins, Ddel, Dsub))
    if (m == 1):
        values = [Dins[0], Ddel[0], Dsub[0]]
        index = values.index(min(values))
        return [Dins, Ddel, Dsub][index]
    elif (m == 2):
        values = [Dins[0], Ddel[0], Dsub[0], Dtran[0]]
        index = values.index(min(values))
        return [Dins, Ddel, Dsub, Dtran][index]

def distance(w1, w2, m):
    return D(w1, w2, len(w1), len(w2), m)
"""


################################################################################
#   Task 1 & 2
################################################################################

# globals
dic = {}
m = 1
trie = trie_node(None, None)


# init trie and dictionary
def init(dictionary):
    words = readFile(dictionary).split()
    for word in words:
        if word != "":
            trie.insert(word)
    
    for word in words:
        if word != "":
            l = len(word)
            if l in dic:
                dic[l][word] = 0
            else:
                d = {}
                d[word] = 0
                dic[l] = d



# match the given word with some word in the dictionary with the
# minimum edit distance
def match(word, d_range, m):
    if (len(word) in dic and word in dic[len(word)]):
        return (word, 0)
    else:
        results = distance(word, d_range, m)
        while (results == []):
            d_range = 2*d_range
            results = distance(word, d_range, m)
        results = sorted(results, key = lambda d: d[1])
        return results[0]


    

def distance(word, d_range, m):
    P = range(len(word)+1)
    PP = []
    results = []

    for letter in trie.letters:
        D(trie.letters[letter], word, P, PP, results, d_range, m)

    return results




def D(node, word, P, PP, results, d_range, m):
    current = []

    for j in xrange(len(word)+1):
        if j == 0:
            current.append(P[0]+1)
        else:
            Dins = current[j-1] + 1
            Ddel = P[j] + 1

            if word[j-1] != node.char:
                Dsub = P[j-1] + 1
            else:                
                Dsub = P[j-1]
            
            if (m == 1):
                currentRow.append(min(Dins, Ddel, Dsub))
            else:
                Dtran = sys.maxint
                if (j - 2 >= 0):
                    if (word[j-1] == node.parent.char and
                        word[j-2] == node.char):
                        Dtran = PP[j-2] + 1
                current.append(min(Dins, Ddel, Dsub, Dtran))

    if current[-1] <= d_range and node.word != None:
        results.append((node.word, current[-1]))

    if min(current) <= d_range:
        for letter in node.letters:
            D(node.letters[letter], word, current, P, results, d_range, m)


def main(argv):
    m = int(argv[0])
    input = argv[1]
    dictionary = argv[2]
    output = argv[3]

    print output

    init(dictionary)

    result = []
    tokens = readFile(input).split("\n")
    for token in tokens:
        word = match(token, 3, m)[0]
        print word
        result.append(word)

    content = "\n".join(result)
    writeFile(output, content)



if __name__ == "__main__":
    main(sys.argv[1:])

