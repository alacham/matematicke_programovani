import Image

def erathosten_sieve(maxnum):
    sieve = [ 1 for i in range(maxnum)]
    sieve[0] = 0
    sieve[1] = 0
    for i in range(2, int(math.sqrt(maxnum))):
        j = 2 * i
        while j < maxnum:
            sieve[j] = 0
            j += i
    return sieve

def ulam_location(ordnum):
    sr = int(ordnum ** 0.5)
    if sr % 2 == 0:
        sr -= 1
    pw2 = sr ** 2
    diff = ordnum - pw2
    
    x = sr / 2
    y = -(sr / 2)
    if diff == 0:
        pass
    elif diff <= (sr + 1):#10,11,12,13
        #print "prava hrana"
        x += 1
        y += diff-1
    elif diff <= (2*(sr+1)):#14,15,16,17
        #print "horni hrana"
        y += sr
        x -= (diff-(sr+2))
    elif diff <= (3*sr + 2): #18,19,20
        #print "leva hrana"
        x -= sr
        y += sr  - (diff - (2*(sr+1)))
    else:#21,22,23,24
        #print "dolni hrana"
        y -= 1
        x += -(sr+1)+(diff - (3*sr + 2))
    return (x,y)
