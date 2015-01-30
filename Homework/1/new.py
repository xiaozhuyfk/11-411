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
re_full = ""
re_last = ""
re_full_mid = ""

src_dir = "nyt"
res_dir = "hongyul-nyt-new"

def init(path):
    global re_full, re_full_mid;
    global re_last;
    names = readFile(path)
    name_list = names.split('\n')
    for name in name_list:
        if (name != ""):
            re_full += ("\\b" + name + "\\b" + "|")
            
            tokens = name.split(" ")
            re_last += ("\\b" + tokens[1] + "\\b" + "|")
            re_full_mid += ("\\b" + tokens[0] + "\\b" +
                            "\\s.{1,4}\\s" +
                            "\\b" + tokens[1] + "\\b" + "|")
            
    if (not os.path.isdir(res_dir)):
        os.mkdir(res_dir)

    re_full = re_full[0:-1]
    re_full_mid = re_full_mid[0:-1]
    re_last = re_last[0:-1]
    

def replace(path, filename):
    content = ""
    line = readFile(path)

    (content, num_full) = re.subn(re_full, "John Smith", line)
    (content, num_mid) = re.subn(re_full_mid, "John Smith", content)
    if (num_full + num_mid > 0):
        content = re.sub(re_last, "Smith", content)
    
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
    
