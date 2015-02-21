from PIL import Image
from math import sin, cos, radians
import random


def ir(x):
    return int(round(x))

def vector_multip_determ(p1, p2, point):
    diag1 = (p2[0] - p1[0]) * (point[1] - p1[1])
    diag2 = (p2[1] - p1[1]) * (point[0] - p1[0])
    return diag1 - diag2

def is_3rd_right(p1, p2, p3):
    if vector_multip_determ(p1, p2, p3) < 0:
        return True
    return False



def graham_scan(inpoints):
    points = sorted(inpoints)
    hulls = ([], [])
    iters = (iter(points), reversed(points))
    for hull, piter in zip(hulls, iters):
        for i in piter:
            if len(hull) <= 1:
                hull.append(i)
            else:
                while len(hull) > 1 and not is_3rd_right(hull[-2], hull[-1], i):
                    hull.pop()
                hull.append(i)
    #return hulls[1] + hulls[0][1:-1] ## proti smeru rucicek
    return hulls[0] + hulls[1][1:-1] ## po smeru rucicek


def ngram_vertexes(n, dist):
    x, y = (dist, dist)    
    vertsfirst = [(x, y)]
    angle = 360.0 / n
    currangle = 0
    minx, miny = x, y
    for _ in range(n - 1):
        y = y + cos(radians(currangle)) * dist
        x = x + sin(radians(currangle)) * dist
        miny = min(miny, y)
        minx = min(minx, x)
        vertsfirst.append((x, y))
        currangle += angle
    verts = map(lambda x: (x[0] - minx, x[1] - miny), vertsfirst)
    return verts
    
    
    

def chaos_game(vertexes, distancemult, iters=100000, size=None, name='chaosgame.png'):
    if not size:
        size = (256, 256)
    
    im = Image.new("RGB", size)
    
    x = random.randint(0, size[0] - 1)
    y = random.randint(0, size[1] - 1)
    
    for i in range(iters):
        chosen = random.choice(vertexes)
        
        x = (x + chosen[0]) * distancemult
        y = (y + chosen[1]) * distancemult
        
        if i > 100:
            newrgbvals = [0, 0, 0]
            currentcols = im.getpixel((int(round(x)), int(round(y))))
            for colv in range(len("rgb")):
                newrgbvals[colv] = min(256, currentcols[colv] + 16)
            im.putpixel((int(round(x)), int(round(y))), tuple(newrgbvals))
        
    im.save('new' + name)
        

if __name__ == '__main__':
    points = ngram_vertexes(3, 256)
    maxx = reduce(lambda prev, p: max(p[0], prev), points, 0) + 1
    maxy = reduce(lambda prev, p: max(p[1], prev), points, 0) + 1
    
    print points, maxx, maxy
    
    chaos_game(points, 1.0 / 2, size=(int(round(maxx)), int(round(maxy))))
    
