import sys
from collections import Counter
from math import log

def train(s):
    tagCounter = Counter()
    tokensCounter = {}
    for line in s.split("\n"):
        tokens = line.split()
        if len(tokens) == 0:
            continue
        tag = tokens[0]
        tokens.pop(0)

        tagCounter.update([tag]);
        if tag not in tokensCounter:
            tokensCounter[tag] = Counter()
        tokensCounter[tag].update(tokens)
    return tagCounter, tokensCounter

def prepare((tagCounter, tokensCounter)):
    den = log(len(tagCounter) + sum(tagCounter.values()))
    print tagCounter
    tagLogs = {}
    for tag in tagCounter:
        tagLogs[tag] = log(tagCounter[tag] + 1) - den

    tokenLogs = {}
    tagDefaults = {}
    for tag in tokensCounter:
        tokenLogs[tag] = {}
        den = log(len(tokensCounter[tag]) + sum(tokensCounter[tag].values()))
        
        tagDefaults[tag] = -den
        for token in tokensCounter[tag]:
            tokenLogs[tag][token] = log(tokensCounter[tag][token] + 1) - den

    return (tagLogs, tagDefaults, tokenLogs)

def classify(tokens, (tagLogs, tagDefaults, tokenLogs)):
    # scores = {}
    maxScore = None
    maxTag = None
    
    for tag in tagLogs:
        n = tagLogs[tag]
        for token in tokens:
            #print tokenLogs[tag].get(token, tagDefaults[tag])

            n += tokenLogs[tag].get(token, tagDefaults[tag])
        if maxScore == None or n > maxScore:
            maxScore = n
            maxTag = tag
        print tag, n
    return maxTag

def readfile(filename):
    with open(filename) as f:
        return f.read()
    return ""

def main():
    # trainFilename = sys.argv[1]
    # testFilename  = sys.argv[2]

    trainFilename = "train2.txt"
    testFilename =  "test2.txt"

    # print train(readfile(trainFilename))
    prepared = prepare(train(readfile(trainFilename)))
    predicted = []
    correct = []


    for line in readfile(testFilename).split("\n"):
        if (len(line)) == 0:
            continue
        tokens = line.split()
        correct += [tokens.pop(0)]
        predicted +=  [classify(tokens, prepared)]

    print predicted
    print correct

    nom = 1.0 * sum([t[0] == t[1]
        for t in zip(correct, predicted)])
    print "accuracy=%3.2f" % (nom / len(correct))

    for tag in set(predicted + correct):
        nom = 1.0 * sum([tag == t[0] and tag == t[1]
            for t in zip(correct, predicted)])
        prc =  nom / sum([tag == t for t in predicted])
        rcl =  nom / sum([tag == t for t in correct])
        print "%s\tprecision=%3.2f, recall=%3.2f" % (tag, prc, rcl)



    return

if __name__ == '__main__':
    main()
