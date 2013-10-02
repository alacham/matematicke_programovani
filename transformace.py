
import numpy as np
import copy
import svgwrite
from math import degrees, radians, cos, sin

from chaos_game import ngram_vertexes



def multiply_shift(a, b, howmuch):
    x = b[0] - a[0]
    y = b[1] - a[1]
    return [howmuch * x, howmuch * y]

class Line:    
    def __init__(self, p1, p2):
        self.x1, self.y1 = p1
        self.x2, self.y2 = p2
    
    def to_svg(self, svgdwg, offset):
        dwg = svgdwg
        dwg.add(dwg.line((self.x1 + offset, self.y1 + offset), (self.x2 + offset, self.y2 + offset), stroke=svgwrite.rgb(10, 10, 16, '%')))
        
    def apply_transform(self, matr):
        p1m = np.mat("%f ; %f; 1" % (self.x1, self.y1))
        p2m = np.mat("%f ; %f; 1" % (self.x2, self.y2))
        
        p1t = matr * p1m
        p2t = matr * p2m
        
        self.x1, self.y1 = p1t[0, 0], p1t[1, 0]
        self.x2, self.y2 = p2t[0, 0], p2t[1, 0]
    
    def length(self):
        a = (self.x1 - self.x2) ** 2
        b = (self.y1 - self.y2) ** 2
        return (a + b) ** 0.5
    
    @property
    def p1(self):
        return self.x1, self.y1
    
    @property
    def p2(self):
        return self.x2, self.y2



class Polygon:
    def __init__(self, plist):
        self.lines = []
        for i in range(len(plist)):
            self.lines.append(Line(plist[i], plist[(i + 1) % len(plist)]))
    
    def to_svg(self, svgdwg, offset):
        for l in self.lines:
            l.to_svg(svgdwg, offset)
    
    def apply_transform(self, matr):
        for l in self.lines:
            l.apply_transform(matr)
    
    def points(self):
        points = []
        for l in self.lines:
            points.append(l.p1)
        return points


def shiftMatrix(x=0, y=0):
    return np.mat("1 0 %f; 0 1 %f; 0 0 1" % (x, y))

def rotationMatrix(degs):
    rads = radians(degs)
    return np.mat("%f %f 0; %f %f 0; 0 0 1" % (cos(rads), -sin(rads), sin(rads), cos(rads)))

def scaleMatrix(kx=1, ky=1):
    return np.mat("%f 0 0; 0 %f 0; 0 0 1" % (kx, ky))

def reflectionMatrix():
    return np.mat("-1 0 0; 0 1 0; 0 0 1")

def shearMatrix(k):
    return np.mat("1 %f 0; 0 1 0; 0 0 1" % k)


def abcdef2Matrix(a, b, c, d, e, f):
    return np.mat("%f %f %f; %f %f %f; 0 0 1" % (a, b, e, c, d, f))


def composeMatrix(matlist):
    retmat = None
    for mat in matlist:
        if retmat is None:
            retmat = mat
        else:
            retmat = mat * retmat
    return retmat



def snail(): #like in slides
    dwg = svgwrite.Drawing('test.svg')
    rm = rotationMatrix(20)
    sm = scaleMatrix(1.1, 1.1)
    shiftm = shiftMatrix(5, 10)
    shiftm2 = shiftMatrix(50)
    
    am = composeMatrix([rm, sm, shiftm])
    pol = Polygon([(0, 0), (100, 0), (100, 100), (0, 100)])
    pol.to_svg(dwg, 500)
    for i in range(15):
        pol.apply_transform(am)
        pol.to_svg(dwg, 500)
    dwg.save()
    
def ufo():#like in slides
    offset = 120
    dwg = svgwrite.Drawing('ufo.svg')
    rm = rotationMatrix(10)
    sm = scaleMatrix(1.1, 0.8)
    
    am = composeMatrix([rm, sm])
    pol = Polygon([(-50, -50), (50, -50), (50, 50), (-50, 50)])
    pol.to_svg(dwg, offset)
    for i in range(15):
        pol.apply_transform(am)
        pol.to_svg(dwg, offset)
    dwg.save()


def roadsnail(): #like in slides
    offset = 100
    dwg = svgwrite.Drawing('roadsnail.svg')
    rm = rotationMatrix(-10)
    sm = scaleMatrix(0.9, 0.9)
    shiftm = shiftMatrix(50, 50)
    shearm = shearMatrix(1.3)
    
    am = composeMatrix([shearm, rm, sm, shiftm])
    pol = Polygon([(0, 0), (100, 0), (100, 100), (0, 100)])
    pol.to_svg(dwg, offset)
    for i in range(25):
        pol.apply_transform(am)
        pol.to_svg(dwg, offset)
    dwg.save()


def recurse_transformations(polygon, canvas, n=10, offset=0):
    if  n == 0 or polygon.lines[0].length() <= 5 :
        polygon.to_svg(canvas, offset)
        return

    vertices = polygon.points()
    pos = vertices[0]
    
    polygon.apply_transform(shiftMatrix(*map(lambda x:-x, pos)))
    polygon.apply_transform(scaleMatrix(0.5, 0.5))
    polygon.apply_transform(shiftMatrix(*list(pos)))
    
    for v in vertices:
        poly = copy.deepcopy(polygon)
        poly.apply_transform(shiftMatrix(*multiply_shift(pos, v, 0.5)))
        
        recurse_transformations(poly, canvas, n - 1)
    
    return
    
    

def recur_triangle():
    verts = ngram_vertexes(3, 400)
    triang = Polygon(verts)
    dwg = svgwrite.Drawing('triang.svg')
    
    offset = 0
    
    dwg.add(dwg.circle((verts[0][0] + offset, verts[0][1] + offset), r=1, stroke=svgwrite.rgb(255, 0, 0, '%')))
    dwg.add(dwg.circle((verts[1][0] + offset, verts[1][1] + offset), r=1, stroke=svgwrite.rgb(255, 0, 0, '%')))
    dwg.add(dwg.circle((verts[2][0] + offset, verts[2][1] + offset), r=1, stroke=svgwrite.rgb(255, 0, 0, '%')))
        
    
    recurse_transformations(triang, dwg, 7, 100)
    dwg.save()



def star():
    dwg = svgwrite.Drawing('star.svg')
    ssize = 400
    verts = ngram_vertexes(4, ssize)
    triang = Polygon(verts)
    
    transforms = [abcdef2Matrix(0.255, 0, 0, 0.255, ssize * 0.3726, ssize * 0.6714),
                  abcdef2Matrix(0.255, 0, 0, 0.255, ssize * 0.1146, ssize * 0.2232),
                  abcdef2Matrix(0.255, 0, 0, 0.255, ssize * 0.6306, ssize * 0.2232),
                  abcdef2Matrix(0.370, -0.642, 0.642, 0.370, ssize * 0.6356, ssize * -0.0061)]
    
    general_recur(triang, 14, dwg, 0, scaleMatrix(1, 1), transforms)
    dwg.save()
    
def fern():
    dwg = svgwrite.Drawing('fern.svg')
    ssize = 200
    verts = ngram_vertexes(3, ssize)
    triang = Polygon(verts)
    
    transforms = [abcdef2Matrix(0.849, 0.037, -0.037, 0.849, ssize * 0.075, ssize * 0.183),
                  abcdef2Matrix(0.197, -0.226, 0.226, 0.197, ssize * 0.4, ssize * 0.049),
                  abcdef2Matrix(-0.15, 0.283, 0.26, 0.237, ssize * 0.575, ssize * 0.084),
                  abcdef2Matrix(0, 0, 0, 0.16, ssize * 0.5, ssize * 0)]
    
    general_recur(triang, 10, dwg, 0, scaleMatrix(1, 1), transforms)
    general_recur(triang, 0, dwg, 0, scaleMatrix(1, 1), transforms)
    general_recur(triang, 1, dwg, 0, scaleMatrix(1, 1), transforms)
#    general_recur(triang, 2, dwg, ssize, scaleMatrix(1,1), transforms)
#    general_recur(triang, 3, dwg, ssize, scaleMatrix(1,1), transforms)
    dwg.save()
    

def general_recur(polyg, howmany, canvas, offset, curtransf, transforms):
    l1 = copy.copy(polyg.lines[0])
    l2 = copy.copy(polyg.lines[-1])
    l1.apply_transform(curtransf)
    l2.apply_transform(curtransf)
    ll = l1.length()
    ll2 = l2.length()
    
    if  howmany == 0 or (ll <= 3 or ll2 <= 3):
#        print howmany
        if ll > 10 and ll2 > 10:
            return
        p = copy.deepcopy(polyg)
        p.apply_transform(curtransf)
        p.to_svg(canvas, offset)
#        print polyg.points()
        return

#    pos = polyg.points()[0]
    for t in transforms:
        tr = t * curtransf
        general_recur(polyg, howmany - 1, canvas, offset, tr, transforms)



def recurse_transformations2(polygon, canvas, n=10, offset=0):
    if  n == 0 or polygon.lines[0].length() <= 5 :
        polygon.to_svg(canvas, offset)
        return

    vertices = polygon.points()
    pos = vertices[0]
    
    polygon.apply_transform(shiftMatrix(10, 10))
    polygon.apply_transform(scaleMatrix(0.7, 0.7))
    #print shiftMatrix(*list(pos))
    polygon.apply_transform(shiftMatrix(*list(pos)))
    
    for v in vertices:
        poly = copy.deepcopy(polygon)
        poly.apply_transform(shiftMatrix(*multiply_shift(pos, v, 0.5)))
        
        recurse_transformations2(poly, canvas, n - 1)
    
    return

def ctverce():
    dwg = svgwrite.Drawing('ctverce.svg')
#    rm = rotationMatrix(20)
    sm = scaleMatrix(1.3, 1.3)
    shiftm = shiftMatrix(0.4, 0.4)
#    shiftm2 = shiftMatrix(50)
    
    am = composeMatrix([sm, shiftm])
    pol = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    pol2 = copy.deepcopy(pol)
    pol2.apply_transform(reflectionMatrix())
        
    pol2.to_svg(dwg, 200)
    for i in range(15):
        pol.apply_transform(am)
        
        pol2 = copy.deepcopy(pol)
        pol2.apply_transform(reflectionMatrix())
        
        pol2.to_svg(dwg, 200)
    dwg.save()


if __name__ == '__main__':
    ctverce()
#    fern()
#    star()
    
    


