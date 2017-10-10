import time
#-----------------------------------------------------------------------------------------------------------------------
#interpreting the input to make a list L containing strings, a number n containing the number of strings, and a list a
#and b for storing the intervals between
def preproc(S):
    L=[]
    n=0
    i=0
    A=[]
    B=[]
    while i < len(S):
        if S[i]=='"':
            n+=1
            L.append('')
            i+=1
            while S[i]!='"':
                L[n-1]+=S[i]
                i+=1
            i+=1
        if i<len(S):
            if S[i]=='[':
                i+=1
                A.append('')
                B.append('')
                while S[i]!=',':
                    A[n-1]+=S[i]
                    i+=1
                i+=1
                while S[i]!=']':
                    B[n-1]+=S[i]
                    i+=1
                i+=1

    a=[int(x) for x in A]
    b=[int(x) for x in B]
    return [L,a,b]

def matches(article,L,a,b,id):
        n=len(L)
        i=0
        # actual starting indices of Strings S1 to Sn in current occurrence
        position=[-1]*n
        # first possible starting position of Si
        start=[0]*n
        # last possible starting position of Si
        match_list=[]
        end=[len(article)]*n
        while (start[0]<len(article)):
            # find first occurrence of string i in between possible indices
            position[i]=article.find(L[i],start[i],end[i])
            if position[i]>=0:
                if i+1==n:
                    match_list.append((position[0],(position[n-1] + len(L[n-1])),id)) #store match
                    # new possible start position = last actual start position + 1
                    start[i]=position[i]+1
                else:
                    # if we didn't reach n yet go to next string and update
                    start[i+1]=position[i]+len(L[i])+a[i]
                    end[i+1]=start[i+1]+b[i]-a[i]+len(L[i+1])   #possible start and end positions
                    i+=1
            else:                                       #we didn't find a match
                i=i-1                                   #so we go back to last input String
                if i<0:
                    break
                else:
                    start[i]=position[i]+1
        return(set(match_list))

QueriesCAT=['"cat"[0,10]"are"[0,10]"to"','"cat"[0,100]"anatomy"','"china"[30,150]"washington"','"english"[0,200]"cat"','"kitten"[15,85]"cat"[0,100]"sire"[0,200]"oxford"']

QueriesA=['"arnold"[0,10]"schwarzenegger"[0,10]"is"','"apache"[0,100]"software"','"aarhus"[30,150]"denmark"','"english"[0,100]"alphabet"','"first"[0,85]"letter"[0,100]"alphabet"[0,200]"consonant"']

QueriesWIKI=['"elephants"[0,20]"are"[0,20]"to"','"technical"[0,20]"university"[0,20]"denmark"','"testing"[0,20]"with"[0,20]"a"[0,30]"lot"[0,4]"of"[0,5]"words"','"stress"[0,250]"test"','"object"[10,200]"application"[0,100]"python"[10,200]"system"[0,100]"computer"[0,10]"science"[0,150]"linux"[0,200]"ruby"']

S=QueriesWIKI[0]
t0 = time.time()
[L, a, b] = preproc(S)
with open("preprocessed_files/wikiPedia.txt", encoding="utf8") as input:
    with open("preprocessed_files/articleIDs.txt", encoding="utf8") as id:
        c=0
        output=open("output.txt",'w',encoding="utf8")
        article=input.readline()
        currentid=id.readline()
        while article !='':
            match_set = matches(article,L,a,b,currentid)
            for [i, j,mid] in match_set:
                output.write(str(mid)+'    ' + article[i:j] + '\n')
                c = c + 1
            article = input.readline()
            currentid = id.readline()  # go to next file
            output.flush()
        t1=time.time()
        output.close()
        filename=''
        for listlen in range(len(L)):
            if listlen==(len(L)-1):
                filename=filename+L[listlen]
            else:
                filename=filename+L[listlen]+str(a[listlen])+str(b[listlen])
        outputnew=open(filename+".txt", 'w', encoding="utf8") #make a new file - store number of matches, time and results
        outputnew.write('#results='+ str(c) + '    ' + 'time=' + str(t1-t0)+'\n')
        with open("output.txt", encoding="utf8") as out:
            line = out.readline()
            while line != '':
                outputnew.write(line)
                line = out.readline()
