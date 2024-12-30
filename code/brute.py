
def brute_2d(points,lower_left,upper_right):
    ans=[]
    for point in points:
        if lower_left[0]<=point[0]<=upper_right[0] and \
            lower_left[1]<=point[1]<=upper_right[1]:
            ans.append(point)
    return ans