import sys

numlist = []

with open(sys.argv[1]) as f:
    for i in f:
        numlist += map(int, i.split())

numbers = {}
prev = 0
successors = {}
nextadds = {}


for j in numlist:
    numbers[j] = numbers.get(j, 0) + 1
    if prev:
        successors[(prev, j)] = successors.get((prev, j), 0) + 1
        nextadds[j + prev] = nextadds.get(j + prev, 0) + 1
    prev = j


print numbers
stuples = sorted(successors.items(), key=lambda (k, v):(v, k))
print stuples, len(stuples)
print nextadds
