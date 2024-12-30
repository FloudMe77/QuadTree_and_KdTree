import math
t=[2,2,2,2,5,7,9,10,10,10,20,30,30,30]
def bsearch_right(t,val):
    p=0
    r=len(t)-1
    while p<r:
        
        i=math.ceil((p+r)/2)
        print(i)
        if t[i]<=val:
            p=i
        else:
            r=i-1
    return p
print(bsearch_right(t,30))