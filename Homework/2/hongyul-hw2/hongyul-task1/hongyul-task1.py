# hw2
# hongyul-task1.py
# Hongyu Li

import os, sys, re, nltk, math

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
#   Some Util functions
################################################################################

# sort the given dictionary
def get_rank(dic):
    return sorted(dic.items(), key = lambda d: d[1])[::-1]


# A helper function to get frequencies of different tokens
def initNGram(text):
    unigram = {}
    bigram = {}
    trigram = {}
    
    content = " ".join(text.split("\n"))
    tokens = content.split(" ")

    while ("" in tokens): tokens.remove("")

    for i in xrange(len(tokens)):
        unitoken = tokens[i]
        bitoken = ""
        tritoken = ""
        if i == 0:
            bitoken = "$start$ " + unitoken
            tritoken = "$start$ $start$ " + unitoken
        elif i == 1:
            tritoken = "$start$ " + tokens[0] + " " + tokens[1]
        else:
            bitoken = tokens[i-1] + " " + unitoken
            tritoken = tokens[i-2] + " " + tokens[i-1] + " " + unitoken

        bitoken = bitoken
        tritoken = tritoken
        
        if (unitoken in unigram):
            unigram[unitoken] += 1
        else:
            unigram[unitoken] = 1

        if (bitoken in bigram):
            bigram[bitoken] += 1
        else:
            bigram[bitoken] = 1

        if (tritoken in trigram):
            trigram[tritoken] += 1
        else:
            trigram[tritoken] = 1 

    return (unigram, bigram, trigram)



# A helper function to get unigrams, bigrams and trigrams
def initNGramList(text):
    unigram = []
    bigram = []
    trigram = []
    
    content = " ".join(text.split("\n"))
    tokens = content.split(" ")

    while ("" in tokens): tokens.remove("")

    for i in xrange(len(tokens)):
        unitoken = tokens[i]
        bitoken = ""
        tritoken = ""
        if i == 0:
            bitoken = "$start$ " + unitoken
            tritoken = "$start$ $start$ " + unitoken
        elif i == 1:
            tritoken = "$start$ " + tokens[0] + " " + tokens[1]
        else:
            bitoken = tokens[i-1] + " " + unitoken
            tritoken = tokens[i-2] + " " + tokens[i-1] + " " + unitoken

        bitoken = bitoken
        tritoken = tritoken
        
        unigram.append(unitoken)
        bigram.append(bitoken)
        trigram.append(tritoken)

    return (unigram, bigram, trigram)
    


################################################################################
#   Task 2 --- subtask 1
################################################################################

def subtask1():
    print "################################################################################"
    print "#                                 subtask 1                                    #"
    print "################################################################################"
    print
    
    filepath = "train/games.txt"
    text = readFile(filepath)
    (unigram, bigram, trigram) = initNGram(text)

    uni_rank = get_rank(unigram)[:6]
    bi_rank = get_rank(bigram)[:6]
    tri_rank = get_rank(trigram)[:6]

    print ("Unigram: %d, Bigram: %d, Trigram: %d" % (len(unigram), len(bigram), len(trigram)))
    print
    print uni_rank
    print bi_rank
    print tri_rank
    print

subtask1()



################################################################################
#   Task 2 --- subtask 2 & 3
################################################################################

# prepare training files
def init():
    files = os.listdir("train")
    
    for filename in files:
        if (filename.endswith(".txt") and (not filename.startswith("TrainingFile"))):
            filepath = "train/TrainingFile_" + filename
            if (not os.path.isfile(filepath)):
                content = ""
                for name in files:
                    if (name != filename and name.endswith(".txt")):
                        path = "train/" + name
                        content += readFile(path)
                writeFile(filepath, content)
            


# replace the infrequent words in text with UNKOWN
def replace_infrequent(text, infrequent):
    content = " ".join(text.split("\n"))
    tokens = content.split(" ")
    for i in xrange(len(tokens)):
        word = tokens[i]
        if word in infrequent:
            tokens[i] = "UNKNOWN"
    content = " ".join(tokens)
    return content


# calculate interpolated perplexity
def perplexity(unigrams, bigrams, trigrams,
               freq_uni, freq_bi, freq_tri,
               lambda0, lambda1, lambda2, lambda3):
    V1 = len(freq_uni)
    V2 = len(freq_bi)
    V3 = len(freq_tri)
    s = 0.0
    n = 0

    for i in xrange(len(unigrams)):
        u = unigrams[i]
        b = bigrams[i]
        t = trigrams[i]
        p3 = probability(t, freq_tri, V1) * lambda3
        p2 = probability(b, freq_bi, V2) * lambda2
        p1 = probability(u, freq_uni, V3) * lambda1
        p0 = float(lambda0)/V1

        lq = math.log(p3+p2+p1+p0)
        s += lq
        n += 1

    return math.exp(- s / n)


# calculate probability according to the frequency
def probability(u, freq, V):
    p = 0.0
    if u in freq:
        p = (freq[u] + 1.0)/(2 * V)
    else:
        p = 1.0/(2 * V)
    return p


def getNGrams(ngramList):
    ngram = {}
    for word in ngramList:
        if word in ngram:
            ngram[word] += 1
        else:
            ngram[word] = 1
    return ngram
        

# split the given contents in half
def splitFile(content):
    firstL = content.split("\n")[:26]
    secondL = content.split("\n")[26:]

    first = " ".join(firstL)
    second = " ".join(secondL)

    return (first, second)


# train the given contents
def train(content):
    (freq_unigram, freq_bigram, freq_trigram) = initNGram(content)
    
    infrequent = set([])
    for word in freq_unigram:
        if freq_unigram[word] < 5:
            infrequent.add(word)

    content = replace_infrequent(content, infrequent)
    return initNGram(content)


# test on the test text with trained frequency records
def test(training, test, lambda0, lambda1, lambda2, lambda3):
    (freq_unigram, freq_bigram, freq_trigram) = train(training)

    (unigram_test, bigram_test, trigram_test) = initNGramList(test)
        
    perp = perplexity(unigram_test, bigram_test, trigram_test,
                      freq_unigram, freq_bigram, freq_trigram,
                      lambda0, lambda1, lambda2, lambda3)

    print ("Perplexity: %f" % perp)
    print


def main(argv):
    init()

    if (len(argv) == 6):
        # This part is for subtask 2
        print "################################################################################"
        print "#                                 subtask 2                                    #"
        print "################################################################################"
        print 
        lambda0 = float(argv[0])
        lambda1 = float(argv[1])
        lambda2 = float(argv[2])
        lambda3 = float(argv[3])
        testFile = argv[4]
        trainingFile = argv[5]

        src_dir = "train"
        files = os.listdir(src_dir)
        for filename in files:
            if (filename.endswith(".txt") and
                (not filename.startswith("TrainingFile"))):
                
                print ("Testing %s" % filename)
                testFile = src_dir + "/" + filename
                trainingFile = src_dir + "/TrainingFile_" + filename
        
                trainingContent = readFile(trainingFile)
                testContent = readFile(testFile)

                test(trainingContent, testContent, lambda0, lambda1, lambda2, lambda3)

        # This part is for subtask 3
        print "################################################################################"
        print "#                                 subtask 3                                    #"
        print "################################################################################"
        print 
        content = readFile(testFile)
        first, second = splitFile(content)
        print ("Testing on second ...")
        test(first, second, lambda0, lambda1, lambda2, lambda3)
        print ("Testing on first ...")
        test(second, first, lambda0, lambda1, lambda2, lambda3)

        
        
    


if __name__ == "__main__":
    main(sys.argv[1:])
