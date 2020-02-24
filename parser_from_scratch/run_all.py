import os
import glob
count=0
filenames = glob.glob("../java_compiler/test/*")
print(filenames)
for filename in filenames:
    os.system("python uncomment.py "+filename+ " > "+filename+"u")
    os.system("rm "+filename)
    os.system("mv "+filename+"u"+" "+filename)
    try:
        os.system("/home/harsh/Skillate/python_vir/venv/bin/python parser_hack.py "+filename+" > a")
        os.system("cat a | tail -n 1 > b")
        f = open("b")
        line = f.readline()
        if(line == "None\n"):
            count+=1
            print(filename)
    except:
        print("/home/harsh/Skillate/python_vir/venv/bin/python parser_hack.py",filename)
        print("error")
        os.system("which python")

        count+=1

print("no of errors",count)