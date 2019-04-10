def binary_search(lis1, left, right, num1):

    if left > right:
        return -1
    mid = (left + right) // 2
    if num1 < lis1[mid]:
        right = mid - 1
    if num1 > lis1[mid]:
        left = mid + 1
    else:
        return mid
    return binary_search(lis1, left, right, num1)


lis1 = [1, 2, 3, 4, 5]
print(lis1)
lis1.sort()
print(lis1)
while 1:
    # keeping testing
    num = int(input('Input the number you wanna find:'))
    res = binary_search(lis1, 0, len(lis1)-1, num)
    if res == -1:
        print('No this number')
    else:
        print('Found, the ref.No is '+str(res+1))
