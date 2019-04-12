from itertools import combinations

color_class = ['*', 'c1', 'c2']
root_class = ['*', 'r1', 'r2', 'r3']
sound_class = ['*', 's1', 's2', 's3']

stream = []
for num_c in color_class:
    for num_r in root_class:
        for num_s in sound_class:
            stream.append([num_c, num_r, num_s])
print(stream)

K = []

#  Remind! Only if member3[0] and member3[1] have different number of '*' will lead to redundancy "冗余"

for k in range(4):
    k += 1
    list_k = list(combinations(stream, k))  # choose n*[k*[1,2,3]] to form a new list
    count = len(list_k)  # Initialise count as length of list_k
    for member1 in list_k:
        stream_k = [idx for idx in member1]  # choose each k*[1,2,3] to form a new list
        list_k2 = list(combinations(stream_k, 2))  # choose 2*[1,2,3] to form a new list
        for member3 in list_k2:  # Firstly, if without '*', we don't need to subtract count
            if '*' in member3[0] or '*' in member3[1]:
                if member3[0] == ['*', '*', '*'] or member3[1] == ['*', '*', '*']:
                    count -= 1  # means redundancy
                    break  # enter next member1, not member3
                location1 = [idx for idx, e in enumerate(member3[0]) if e == '*']  # locate '*'
                location2 = [idx for idx, e in enumerate(member3[1]) if e == '*']
                location = list(set(location1).union(set(location2)))
                list_set = [0, 1, 2]
                step = list(set(list_set).difference())  # to see which position are not '*' in both member3[0] and [1]
                if location1 != [] and location2 != []:  # both have '*'
                    if (len(location1) > len(location2) or len(location1) < len(location2)) and step != [] and member3[0][step[0]] == member3[1][step[0]]:
                        # This means different number of '*' and '*' has overlaps and not '*' position are same
                        count -= 1
                        break
                    continue
                    # enter next member3

                real = 0  # only one member3 has '*'
                for i in step:
                    if member3[0][i] == member3[1][i]:
                        real += 1
                if real == len(step):
                    count -= 1
                    break
    K.append(count)
    print('process %', k)

for i in range(len(K)):
    print('length %d : %d' % (i+1, K[i]))


