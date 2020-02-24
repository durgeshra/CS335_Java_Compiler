import os
import sys
import math
import re
import os.path

inputfolder = sys.argv[1]

with open(inputfolder, "r") as f:
    data = f.read()
    output = ""
    
    n = len(data)
    i=0
    while i<n:
        if i!=n-1 and data[i]=='/' and data[i+1]=='*':
            i=i+2
            closed = 0
            newlines = 0
            while i<n-1:
                if data[i]=='*' and data[i+1]=='/':
                    closed = 1
                    i+=1    
                    break
                if data[i]=='\n':
                    newlines+=1
                i+=1
            if not closed:
                print("UNCLOSED COMMENT!")
                quit()
            else:
                for l in range(newlines):
                    output += '\n'
        elif i!=n-1 and data[i]=='/' and data[i+1]=='/':
            i=i+2
            while i<n:
                if data[i]=='\n':
                    output+='\n'
                    # i+=1
                    break
                i+=1
        else:
            output+=data[i]
        i+=1    


    print(output)