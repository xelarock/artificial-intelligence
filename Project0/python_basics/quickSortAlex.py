
def quickSort(lst):
    print len(lst)-1
    if len(lst) <= 1:
        return lst
    smaller = [x for x in lst[:len(lst)-1] if x < lst[len(lst)-1]]
    larger = [x for x in lst[:len(lst)-1] if x >= lst[len(lst)-1]]
    return quickSort(smaller) + [lst[len(lst)-1]] + quickSort(larger)

# Main Function
if __name__ == '__main__':
    lst = [2, 4, 5, 1, 2]
    print quickSort(lst)
