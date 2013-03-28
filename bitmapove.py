import Image
import math
from usecky import Usecka, prunik_usecek

def kruh_impl():
    im = Image.new("RGB", (256, 256))
    
    for i in range(-128, 128):
        for j in range(-128, 128):
            if i ** 2 + j ** 2 <= 128 ** 2:
                im.putpixel((i + 128, j + 128), (i + 128, 0, j + 128))
    im.show()

def kruznice_impl():
    im = Image.new("RGB", (256, 256))
    
    for i in range(-128, 128):
        for j in range(-128, 128):
            if round((i ** 2 + j ** 2) ** 0.5) == 128:
                im.putpixel((i + 128, j + 128), (i + 128, 0, j + 128))
    im.show()
    
def kruznice_param():
    im = Image.new("RGB", (256, 256))
    
    iteri = 0
    while iter <= 2 * math.pi:
        i = int(round(127 * math.cos(iteri)))
        j = int(round(127 * math.sin(iteri)))
        print i, j
        im.putpixel((i + 128, j + 128), (i + 128, 0, j + 128))
        iter += 0.001
    im.show()
    
def spirala_param():
    im = Image.new("RGB", (512, 512))
    
    iteri = 0
    r = 0
    while iter <= 6 * math.pi:
        i = int(round(r * math.cos(iter)))
        j = int(round(r * math.sin(iter)))
        print i, j
        im.putpixel((i + 128, j + 128), (i + 128, 0, j + 128))
        iter += 0.001
        r += math.pi * 0.001 * 2
    im.show()
    

def trojuhelnik(a=30):
    im = Image.new("RGB", (256, 256))
    
    
    vrchni = ((a ** 2) - (a / 2.0) ** 2) ** 0.5
    
    for i in range(-128, 128):
        for j in range(-128, 128):
            if 0 <= j <= ((a ** 2) - (a / 2.0) ** 2) ** 0.5 and (-a * 0.5) < i < (a * 0.5) and (j <= (vrchni / (0.5 * a)) * i + vrchni) and (j <= -(vrchni / (0.5 * a)) * i + vrchni):
                im.putpixel((i + 128, j + 128), (i + 128, 0, j + 128))
    im.show()
    
    
def elipsa_impl():
    im = Image.new("RGB", (512, 512))
    
    for i in range(-256, 256):
        for j in range(-256, 256):
            if i ** 2 + j ** 2 + i * j <= 128 ** 2:
                im.putpixel((i + 256, j + 256), (i + 128, 0, j + 128))
    im.show()

def mnohouhelnik(body):
    usecky = [Usecka(body[i], body[i + 1]) for i in range(0, len(body) - 1)]
    usecky += [Usecka(body[0], body[-1])]
    maxx = max(body, key=lambda a: a[0])[0]
    maxy = max(body, key=lambda a: a[1])[1]
    im = Image.new("RGB", (maxx + 1, maxy + 1))
    pix = im.load()
    for y in xrange(maxy + 1):
        primka = Usecka((0, y), (maxx, y))
        pruniky = []
        for i in xrange(len(usecky)):
            segm = usecky[i]
            # dva pruniky na stejny bod chci jen pro body ktere jsou y-extremem mezi sousedy
            if segm.y1==y or segm.y2 == y:
                if segm.y1 == y:
                    pruniky.append(segm.x1)
                else:
                    y1 = segm.y1
                    y2 = segm.y2 # == usecky[(i+1)%len(usecky)].y1
                    y3 = usecky[(i+1)%len(usecky)].y2
                    if y2 == max(y1,y2,y3) or y2 == min(y1,y2,y3):
                        pruniky.append(segm.x2)
            else:
                prunik = prunik_usecek(primka,segm)
                if prunik:
                    pruniky.append(int(round(prunik[0])))
        if not pruniky:
            continue
        prulen = len(pruniky)
        pruniky.sort()
        currindex = 0 #znaci kolik pruniku mela horizontalni cara az po prave probirane x
        val = pruniky[0]
        for x in xrange(maxx + 1):
            while val == x:
                currindex += 1
                if currindex == prulen:
                    break
                val = pruniky[currindex]
            if currindex % 2 == 1:#kresli
                pix[x, y] = (255, 255, 255)
        #print time.time() - ct
    im.show()


def konvoluce(inname, konvmaticeperrgb):
    if len(konvmaticeperrgb) == 1:
        konvmatice = 3 * konvmaticeperrgb
    else:
        konvmatice = konvmaticeperrgb
    print konvmatice
    im = Image.open(inname)
    imo = Image.new("RGB", (im.size[0], im.size[1]))
    shift = len(konvmatice[0]) / 2
    print shift
    for y in range(shift, im.size[1] - shift):
        for x in range(shift, im.size[0] - shift):
            newrgbvals = [0, 0, 0]
            for yk in range(-shift, shift + 1):
                for xk in range(-shift, shift + 1):
                    oldrgb = im.getpixel((x + xk, y + yk))
                    #print 'get',oldrgb
                    #print oldrgb
                    for colv in range(len("rgb")):
                        #print yk, xk, colv, konvmatice[colv][yk+shift][xk+shift]
                        newrgbvals[colv] += oldrgb[colv] * konvmatice[colv][yk + shift][xk + shift]
            #print 'put',newrgbvals
            
            ## special for priklad 1, v prechodech nejsou hrany dost vyrazne aby to slo normalne
            #if abs(sum(newrgbvals)) > 5:
            #    imo.putpixel((x,y),(255,255,255))
            ############### konec pr 1
            
            imo.putpixel((x, y), tuple(newrgbvals))
    imo.save('new' + inname)

#elipsa_impl()

edgedetect = [[[0, 1, 0], [1, -4, 1], [0, 1, 0]]]
edgeenhance = [[[0, -1, 0], [-1, 2, 0], [0, 0, 0]]]

zvyraznimodrou = [[[0, 0, 0], [0, 1, 0], [0, 0, 0]], [[0, 0, 0], [0, 1, 0], [0, 0, 0]], [[0, 0, 0], [0, 10, 0], [0, 0, 0]]]

#konvoluce('skryvacka2.png', edgeenhance)

#konvoluce('skryvacka1.png', zvyraznimodrou)

nuhelbody = [(0, 0), (50,50), (100, 290), (200, 200), (320, 300), (250, 150), (300, 0), (200, 100)]



mnohouhelnik(nuhelbody)



