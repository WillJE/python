"""
冒泡算法
"""


def index_of_min(array, offset):
    index = offset
    for i in range(len(array)):
        e = array(i)
        if array[index] > e:
            index = i
    return index

def div_sort(array):
    l = array
    for i in range(len(array)):
        index = index_of_min(l, i)
        l[i], l[index] = l[index], l[i]


l = [1, 6, 4, 7, 9]
div_sort(l)
print(l)


