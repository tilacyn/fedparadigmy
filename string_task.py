def verbing(s):
    if len(s)<3:
        return s
    if s.endswith("ing"):
        return s+"ly"
    else:
        return s+"ing"

def front_back(a,b ):
    a1=len(a)//2+len(a)%2
    b1=len(b)//2+len(b)%2
    s=a[0:a1]+b[0:b1]+a[a1:len(a)]+b[b1:len(b)]
    return s


def not_bad(s):
    n=s.find("not")
    b=s.find("bad")
    if n<b:
        return s[0:n]+"good"+s[b+3:len(s)]
    else:
        return s

     
