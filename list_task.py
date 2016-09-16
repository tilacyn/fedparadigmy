def remove_adjacent(lst):
    l=[]
    l.append(lst[0])
    for i in range(1,len(lst)):
        if lst[i]!=l[-1]:
            l.append(lst[i])
    return l

def linear_merge(lst1, lst2):
    lst=[]
    a1=0; a2=0
    while a1<len(lst1)and a2<len(lst2):
        
        if lst1[a1]<=lst2[a2]:
            lst.append(lst1[a1])
            a1=a1+1
        else:
            lst.append(lst2[a2])
            a2=a2+1
            
    if a1>=len(lst1):
            lst.extend(lst2[a2:])
    if a2>=len(lst2):
            lst.extend(lst1[a1:])
            
    return lst

