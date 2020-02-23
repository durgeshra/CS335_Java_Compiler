f = open("parser_durgesh.py")
f1 = open("fixed.py","w")
line = f.readline()
st = ""
while(line):
    arr = line.split(" ")

    if(arr[0]=='def'):
        ele = arr[1][2:]
        na = ""
        i=0
        while(ele[i]!='(' and ele!=' '):
            na+=ele[i]
            i+=1
    if(line!='\n' and line[-2]=="'"):
        st+=line + '\t' + "p[0]=tuple([\""+na+"\"]+p[1:])" + "\n"
    else:
        st +=line
    line = f.readline()
f1.write(st)
