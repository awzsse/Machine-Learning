from itertools import combinations


class X:
    def __init__(self, value):
        self.data = value

    def __or__(self, other):
        return self.data | other.data


stream = [0xff,0xf9,0xfa,0xfc,0xcf,0xd7,0xe7,0x7f,
                      0xbf, 0xc9,0xca,0xcc,0xd1,0xd2,0xd4,0xe1,
                      0xe2, 0xe4,0x79,0x7a,0x7c,0xb9,0xba,0xbc,
                      0x4f, 0x57,0x67,0x8f,0x97,0xa7,0x49,0x4a,
                      0x4c, 0x51,0x52,0x54,0x61,0x62,0x64,0x89,
                      0x8a, 0x8c,0x91,0x92,0x94,0xa1,0xa2,0xa4
]

print(stream)

K = []

#  Remind! Only if member3[0] and member3[1] have different number of '*' will lead to redundancy "冗余"

for k in range(3):
    k += 1
    list_k = list(combinations(stream, k))  # choose n*[k*[1,2,3]] to form a new list
    count = len(list_k)  # Initialise count as length of list_k
    for member1 in list_k:
        stream_k = [idx for idx in member1]  # choose each k*[1,2,3] to form a new list
        list_k2 = list(combinations(stream_k, 2))  # choose 2*[1,2,3] to form a new list
        for member3 in list_k2:  # Firstly, if without '*', we don't need to subtract count
            x = X(member3[0])
            y = X(member3[1])
            if (x | y) == x or (x | y) == y:
                count -= 1
                break
    K.append(count)
    print('process %', k)

for i in range(len(K)):
    print('length %d : %d' % (i+1, K[i]))

a = 15
b = 15

c = a | b

print(c)

