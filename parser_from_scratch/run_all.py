import os
import glob
count=0
# filenames = glob.glob("../java_compiler/test/*")
filenames = glob.glob("./problems/*")
mypython="/usr/local/Cellar/python/3.7.6_1/bin/python3.7"
print(filenames)
for filename in filenames:
    os.system("python uncomment.py "+filename+ " > "+filename+"u")
    os.system("rm "+filename)
    os.system("mv "+filename+"u"+" "+filename)
    try:
        os.system(mypython+" parser_hack.py "+filename+" > a")
        os.system("cat a | tail -n 1 > b")
        f = open("b")
        line = f.readline()
        if(line == "None\n"):
            count+=1
            print(filename)
    except:
        print(mypython+" parser_hack.py",filename)
        print("error")
        os.system("which python")

        count+=1

print("no of errors",count)
