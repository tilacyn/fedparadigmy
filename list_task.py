def remove_adjacent(lst):
    i=0;
    while i<len(lst): 
        if lst[i]==lst[i-1]:
                   lst.pop(i)
        i=i+1
    return lst


def linear_merge(lst1, lst2):
    lst=[]
    for i in range(len(lst1)+len(lst2)):
        if len(lst1)==0:
            lst.extend(lst2)
            break
        if len(lst2)==0:
            lst.extend(lst1)
            break
        if lst1[0]<=lst2[0]:
            lst3.append(lst1[0])
            lst1.pop(0)
        else:
            lst.append(lst2[0])
            lst2.pop(0)
    return lst
