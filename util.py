def listSearch(T,keyword, start=0):
    try :
        idx = T.index(keyword,start)
    except : 
        return []
    return [idx] + listSearch(T,keyword,idx+1)