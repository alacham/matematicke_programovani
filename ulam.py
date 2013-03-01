import Image

def erathosten_sieve(maxnum):
    sieve = [ 1 for i in range(maxnum)]
    sieve[0] = 0
    sieve[1] = 0
    for i in range(2, int(maxnum**0.5)):
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

def show_ulam(edge):
    odd = edge % 2
    even = 1-odd
    prvocisla = erathosten_sieve(1 + edge ** 2)
    im = Image.new("RGB", (edge, edge))
    
    # mark middle point (1) by red color
    im.putpixel(((edge / 2)-even, (edge / 2)-even), (255, 0, 0))
    
    for i in range(1, len(prvocisla)):
        if prvocisla[i] == 1:
            x, y = ulam_location(i)
            #print i,':',x,y
            x += (edge / 2)-even
            y += (edge / 2)-even
            #print x,y,edge - 1 - y
            # edge-1-y because y==0 is in UPPER left corner
            im.putpixel((x, edge - 1 - y), (255, 255, 255))
    im.show()

def quarter_ulam_location(ordnum):
    ''' tohle jsem programoval v prvni serii KSI :D
        Podobne ulamove spirale ale, zacina se v rohu
    '''
    isqrt = int(ordnum ** 0.5)
    differ = ordnum - isqrt ** 2
    a = isqrt
    b = 0
    if  differ > a:
        b = a
        a = 2 * a - differ
    else:
        b = differ
    if isqrt % 2 == 0:
        return (b, a)
    else:
        return (a, b)




