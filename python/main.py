# coding: utf-8

def mergesort(L):
    if len(L) <= 1:
        return L
    
    mid = len(L) / 2

    left = mergesort(L[:mid])
    right = mergesort(L[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    m = 0
    n = 0

    
    while m < len(left) and n < len(right):
        if left[m] < right[m]:
            result.append(left[m])
            m=m+1
        else:
            result.append(right[n])
            n=n+1

    result += left[m:]
    result += right[n:]

    return result

L = [2,1,0,38,39,3787,2098,10,88,2876,78]
print(mergesort(L))