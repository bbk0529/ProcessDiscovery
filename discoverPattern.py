def listSearch(T,keyword, start=0):
    try :
        idx = T.index(keyword,start)
    except : 
        return []
    return [idx] + listSearch(T,keyword,idx+1)


def search (L, pl,pr,tl,tr, lm, rm,rep ):
    pl = pl-lm
    pr = pr+rm
    tl = tl-lm
    tr = tr+rm
    pattern=[L[pl : pr], pl, pr]
    target=[L[tl :tr], tl, tr]
    
    lhs = pattern[0][0] == target[0][0]
    rhs = pattern[0][-1] == target[0][-1]
    #print("\t"*rep, rep, pl+1, tl+1, pattern, target, lhs, rhs)
    
    
    if(lhs or rhs) :
        #print("\t"*rep, "expand to the", "left"* lhs, "right" * rhs)
        pattern, target= search(L, pl,pr,tl,tr,lhs,rhs, rep+1) #recursion call
    #else :
        #print("\t"*rep, "pattern found", pattern[0][1: -1],"\n")   
        
    return pattern, target
    


def discoverMaximalRepeat(L) : 
    maximalRepeatSet={}
    A=list(set(L))
    A.sort()
    #print("set of Activities", A)
    L=[''] + L + ['']
    #print("log with paading", L)
    
    for activity in A :
        #print("\nto be started with activity", activity)    
        idx=listSearch(L,activity,0)
        #print("found activity", activity, "in", idx)
        
        for l in range(len(idx)) :  #pi = the position of pattern
            indice=idx[l:]
            pl = indice[0]-1  #pl = pattern -1 to include immediate left 
            pr = indice[0] + 2 # pattern + 1 to include immediate right 
            for ti in indice[1:]: #ti = the position of target 
                tl= ti-1  #adding padding to the immediate left of the target
                tr= ti+2 #adding padding to the immediate right of the target
                pattern, target = search(L, pl, pr, tl, tr, 0,0,0)
                repeatedActivity=','.join(pattern[0][1:-1])
                maximalRepeatSet[repeatedActivity]=maximalRepeatSet.get(repeatedActivity, 0) +1
    return maximalRepeatSet


def discoverSuperMaximalRepeat(maximal_repeat_set) :
    if not maximal_repeat_set : return []
    #print("To be processed here", maximal_repeat_set)
    flag=True  
    super_maximal_repeat_set=[]
    candidate=maximal_repeat_set.pop(0)
    for maximal_repeat in maximal_repeat_set : 
        if candidate  in maximal_repeat :
            #print (candidate, "is in the", maximal_repeat)
            flag=False 
            break
    if flag==True : 
        #print(candidate,"is the element of SuperMaximalRepeatSet")
        super_maximal_repeat_set.append(candidate)
        #print(candidate, "appended in", super_maximal_repeat_set)
        
    super_maximal_repeat_set=super_maximal_repeat_set + discoverSuperMaximalRepeat(maximal_repeat_set)
    #print("returning super_maximal_repeat_set", super_maximal_repeat_set)
    return super_maximal_repeat_set