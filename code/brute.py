
def brute_2d(points,lower_left,upper_right):
    ans=[]
    for point in points:
        flaga = True
        for i in range(len(point)):
            if not lower_left[i]<=point[i]<=upper_right[i]:
                flaga=False 
        if flaga:
            ans.append(point)
    return ans