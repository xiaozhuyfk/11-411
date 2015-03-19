# hw4
# hongyul-hw4.py
# Hongyu Li

import os, sys, re, math
from collections import Counter

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

#globals
dic = {}
mapping = {}
mapping["RED"] = {}
mapping["BLUE"] = {}
types = {}

tag_probability = {}
probability = {}

N = 0
RED = 0
BLUE = 0


def init(path):
    global mapping, types, probability, dic, N, RED, BLUE
    
    content = readFile(path)
    speeches = content.split("\n")
    for speech in speeches:
        if (speech != ""):
            words = speech.split()
            category = words[0]

            if category in types:
                types[category] += 1
            else:
                types[category] = 1
            
            for word in words[1:]:
                if word in mapping[category]:
                    mapping[category][word] += 1
                else:
                    mapping[category][word] = 1

                if word in dic:
                    dic[word] += 1
                else:
                    dic[word] = 1

    for category in mapping:
        tag_denom = math.log(len(types) + sum(types.values()))
        tag_probability[category] = math.log(types[category] + 1) - tag_denom

        if category not in probability:
            probability[category] = {}
        
        frequency = mapping[category]
        denom = math.log(len(frequency) + sum(frequency.values()))

        for word in frequency:
            probability[category][word] = math.log(frequency[word] + 1) - denom

        probability[category]["NEVERFOUND"] = -denom

def classify(path):
    global mapping, types, probability, dic, N, RED, BLUE

    classification = []
    result = []

    content = readFile(path)
    speeches = content.split("\n")
    
    for speech in speeches:
        if (speech != ""):
            words = speech.split()
            category = words[0]
            classification.append(category)
            
            sum_red = tag_probability["RED"]
            sum_blue = tag_probability["BLUE"]
                        
            for word in words[1:]:
                if word in probability["RED"]:
                    sum_red += probability["RED"][word]
                else:
                    sum_red += probability["RED"]["NEVERFOUND"]
                    
                if word in probability["BLUE"]:
                    sum_blue += probability["BLUE"][word]
                else:
                    sum_blue += probability["BLUE"]["NEVERFOUND"]

            print "Speech %d: RED = %0.3f, BLUE = %0.3f" % (speeches.index(speech), sum_red, sum_blue)
            if sum_red > sum_blue:
                result.append("RED")
            else:
                result.append("BLUE")

    return (classification, result)
        


################################################################################
#   Task 1 & 2 & 3
################################################################################

def main(argv):
    trainingFile = argv[0]
    testFile = argv[1]
    
    init(trainingFile);

    (classification, result) = classify(testFile)
    
    print classification
    print result

    correct = 0
    for i in xrange(len(classification)):
        if (classification[i] == result[i]):
            correct += 1
    accuracy = float(correct) / len(result)

    print "Overall Accuracy: %0.3f" % accuracy

    for category in mapping:
        correct = 0
        for i in xrange(len(result)):
            if (result[i] == classification[i] == category):
                correct += 1

        precision = float(correct) / result.count(category)
        recall = float(correct) / classification.count(category)
        print "%s: Precision = %0.3f, Recall = %0.3f" % (category, precision, recall)


if __name__ == "__main__":
    main(sys.argv[1:])

