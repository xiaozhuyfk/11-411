# hongyul-task3.py
# Hongyu Li

import os, sys, re

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


# Globals
name_set = set([])
first = set([])
last = set([])
src_dir = "nyt"
res_dir = "hongyul-nyt-modified"
re_full = ""
re_last = ""

def init(path):
    global re_full;
    global re_last;
    
    names = readFile(path)
    name_list = names.split('\n')
    
    for name in name_list:
        if (name != ""):
            name_set.add(name)
            tokens = name.split(" ")
            first.add(tokens[0])
            last.add(tokens[1])
    if (not os.path.isdir(res_dir)):
        os.mkdir(res_dir)

    re_full = re_full[0:-1]
    re_last = re_last[0:-1]
    

def replace(path, filename):
    content = ""
    line = readFile(path)

    content = re.sub(re_full, "John Smith", line)
    
    words = re.split('(\W+)', content)

    for i in xrange(len(words)):
        word = words[i]
        if (word in first):
            if (i+2 < len(words)):
                if (words[i+1] == " " and
                    (word + " " + words[i+2]) in name_set):
                    content += "John"
                else:
                    content += word
            else:
                content += word
        elif (word in last):
            if (i-2 >= 0):
                firstname = words[i-2]
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

    res_file = res_dir + '/' + filename
    writeFile(res_file, content)
        
def main():
    print "Initializing ..."
    init("names.txt")
    print "Initialization complete!"

    print "Replacing ..."
    files = os.listdir(src_dir)
    for filename in files:
        print "Replacing file %s" % filename
        path = src_dir + "/" + filename
        replace(path, filename)

main()
    
