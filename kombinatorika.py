
#variace, nekdy z drivejska na generovani hesel, mam nekde i v C
def variace(charlist, leng, repeat=False):
    if leng == 1:
        return [ i for i in charlist]
    pws = []
    tmp = variace(charlist, leng - 1, repeat)
    for i in charlist:
        for j in tmp:
            if repeat or i not in j:
                pws.append(i + j)
    return pws


#kombinace - like a boss - lazy way, functional programming
# skoro one-liner
def kombinace(charlist, leng, repeat=False):
    var_res = variace(charlist, leng, repeat)
    return list(set(map(lambda x: "".join(sorted(list(x))), var_res)))


def permutace_1(charlist, passed):
    if len(charlist) == 0:
        print passed
    for i in charlist:
        reduced_chars = charlist[:]
        reduced_chars.remove(i)
        permutace_1(reduced_chars, passed + i)


print variace(['a','b','c','d'],3)
print len(variace(['a','b','c','d'],3))
print kombinace(['a','b','c','d'],3)
