import os
import glob
count=0
# filenames = glob.glob("../java_compiler/test/*")
# filenames = glob.glob("./problems/*")
# filenames = glob.glob("../testcases/*")

# mypython="/usr/local/Cellar/python/3.7.6_1/bin/python3.7"
mypython = "/home/harsh/Skillate/python_vir/venv/bin/python"
print(filenames)
for filename in filenames:
#     os.system("python uncomment.py "+filename+ " > "+filename+"u")
#     os.system("rm "+filename)
#     os.system("mv "+filename+"u"+" "+filename)
    try:
        os.system(mypython+" parser_hack.py -i "+filename+" > a")
        os.system("cat a | tail -n 1 > b")
        f = open("b")
        line = f.readline()
        if(line == "ERROR\n"):
            count+=1
            print(filename)
    except:
        print(mypython+" parser_hack.py",filename)
        print("error")
        os.system("which python")
        count+=1

print("no of errors",count)

# new_ele = ()
# def reduce(ele):
# 	new_ele =()
# new_ele.append(ele[0])
#     if(type(ele) ==str)
#         return tuple([ele])
#     elif(type(ele)==tuple && len(ele)==1):
#         return ele


#     if(len(ele)==2):
#         return reduce(ele[1])
#     else:
#         for data in ele[1:]:
#             new_ele.append(reduce(data))