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
name_set = set([])
first = set([])
last = set([])
re_full = ""
re_full_mid = ""

src_dir = "nyt"
res_dir = "hongyul-nyt-modified"



# Init name sets and regexp
def init(path):
    global re_full, re_full_mid;
    global re_last;
    names = readFile(path)
    name_list = names.split('\n')
    for name in name_list:
        if (name != ""):
            re_full += ("\\b" + name + "\\b" + "|")
            
            tokens = name.split(" ")
            re_full_mid += ("\\b" + tokens[0] + "\\b" +
                            "\\s.{1,4}\\s" +
                            "\\b" + tokens[1] + "\\b" + "|")
            
    if (not os.path.isdir(res_dir)):
        os.mkdir(res_dir)

    re_full = re_full[0:-1]
    re_full_mid = re_full_mid[0:-1]
    

# replace full names and last names for file with given path and filename
def replace(path, filename):
    content = ""
    line = readFile(path)

    # substitute full name
    name_list = []
    name_list += re.findall(re_full, line)
    name_list += re.findall(re_full_mid, line)
    (content, num_full) = re.subn(re_full, "John Smith", line)
    (content, num_mid) = re.subn(re_full_mid, "John Smith", content)

    lastname_set = set([])
    for name in name_list:
        if (name != ""):
            tokens = name.split(" ")
            lastname_set.add(tokens[-1])
            

    # handle single last name replacement
    words = re.split("(\W+)", content)

    # only replace last names that its full name has appeared
    # in the file somewhere
    if (len(name_list) > 0):
        content = ""
        for i in xrange(len(words)):
            word = words[i]
            if (word in lastname_set):
                if (i-2 >= 0):
                    firstname = words[i-2]
                    # If the last name is after a mismatched first name
                    # don't replace it
                    if (words[i-1] == " " and
                        firstname.isalpha() and
                        firstname[0].isupper() and
                        (firstname + " " + word) not in name_set):
                        content += word
                    else:
                        content += "Smith"
                else:
                    content += "Smith"
                    
            else:
                content += word

    # write to file
    res_file = res_dir + '/' + filename
    writeFile(res_file, content)
        
def main():
    print "Initializing ..."
    init("names.txt")
    print "Initialization complete!"

    files = os.listdir(src_dir)
    for filename in files:
        print "Processing file %s" % filename
        path = src_dir + "/" + filename
        replace(path, filename)


        
main()
    
