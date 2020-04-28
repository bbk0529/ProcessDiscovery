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
    #print("\t"*rep, pattern, target, lhs, rhs)
    
    pattern_location=[]
    
    if(lhs or rhs) :
        #print("\t"*rep, "expand to the", "left"* lhs, "right" * rhs)
        pattern, target, pattern_location= search(L, pl,pr,tl,tr,lhs,rhs, rep+1) #recursion call
    else :
        pattern_location=[[pl+1,pr-2],[tl+1,tr-2]]
        #print("\t"*rep, "pattern found", pattern[0][1: -1],pattern_location,"\n")   
    
    return pattern, target, pattern_location
    

    
def discoverMaximalRepeat(L) : 
    maximal_repeat_set={}
    pattern_locations=[]
    A=list(set(L))
    A.sort()
    A.sort(key=len)
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
                pattern, target,pattern_location = search(L, pl, pr, tl, tr, 0,0,0)
                repeated_activity=','.join(pattern[0][1:-1])
                if maximal_repeat_set.get(repeated_activity, False ) == False : 
                    #print('empty')
                    maximal_repeat_set[repeated_activity]={'location' : pattern_location} # if not exist, it crates the data set in the dictionary. 
                else : #if already exist in the dic.
                    for location in pattern_location:
                        if location not in maximal_repeat_set[repeated_activity]['location'] : 
                            maximal_repeat_set[repeated_activity]['location'].append(location)
                #print("updated in the dictionary", repeated_activity, maximal_repeat_set[repeated_activity], "\n\n\n\n")
    for activities in maximal_repeat_set : 
        maximal_repeat_set[activities]['length']=activities.count(',')+1
        #maximal_repeat_set[activities]['repeat']=len(maximal_repeat_set[activities]['location'])         
    
    return maximal_repeat_set





def discoverSuperMaximalRepeat(maximal_repeat_set) :
    maximal_repeat_set.sort()
    maximal_repeat_set.sort(key=len)
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
        
    super_maximal_repeat_set+= discoverSuperMaximalRepeat(maximal_repeat_set)
    #print("returning super_maximal_repeat_set", super_maximal_repeat_set)
    super_maximal_repeat_set.sort()
    super_maximal_repeat_set.sort(key=len)
    return super_maximal_repeat_set



def discoverNearSuperMaximalRepeat(maximal_repeat_data, super_maximal_repeat_set) :
    candidates=list(set(maximal_repeat_data.keys()) - set(super_maximal_repeat_set))
    candidates.sort()
    candidates.sort(key=len)
    near_super_maximal_repeat_set=[]
    for i in candidates : 
        candidate_locations=maximal_repeat_data[i]['location']
        #print(i, candidate_locations)
        target_locations=[]
        for k in set(maximal_repeat_data.keys()) - {i} :
            location=maximal_repeat_data[k]['location']
            target_locations+=location
        target_locations.sort()
        #print("target", target_locations)

        for cl in candidate_locations :
            Flag=True 
            for tl in target_locations : 
                #print("comparision",i,cl,tl)
                if ((tl[0]<=cl[0]) & (cl[1]<=tl[1])) : 
                    #print("\toverlapped", i, cl, tl)
                    Flag=False 
                    break #no more comparision required. 
            if (Flag==True) : 
                #print("\t\tfound nearmaximum", i,cl,tl)
                near_super_maximal_repeat_set.append(i)
                break
                # no more comparision required in Candidate locations 
    return near_super_maximal_repeat_set




def patternDiscover(log) : 
    log=[l for l in log]
    
    mr=discoverMaximalRepeat(log)
    mrs=list(mr.keys())

    smrs=discoverSuperMaximalRepeat(mrs)
    nsmrs=discoverNearSuperMaximalRepeat(mr,smrs)
    
    nsmrs=(nsmrs+ smrs);nsmrs.sort();nsmrs.sort(key=len)
    mrs= list(mr.keys());mrs.sort();mrs.sort(key=len)
    
    
    print("given log T","\n\t", log)
    print("discovered patterns")
    print("\tmaximal repeat set",mrs)
    print("\tsuper maximal repeat set", smrs)
    print("\tnear super maximal repeat set", nsmrs)
    
