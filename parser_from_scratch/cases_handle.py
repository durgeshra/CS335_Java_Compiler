filename = "AES.java"
f = open(filename)
lines = f.read()
prev = ''
last_non = ''
place = 0 
ans = ""
writing = 0
index=-1
start=0
for ele in lines:
    index +=1
    if(ele ==','):
        start = 1
        place = index
    elif(start==1 and ele!=' '):
        if(ele == '}'):
            ans+=lines[:place]
            ans+=lines[place+1:index+1]
        else:
            ans+=lines[:index+1]
        writing = index+1
        start=0

ans+=lines[writing:]
f1 = "cleaned_AES.java"
f1.write(ans)


