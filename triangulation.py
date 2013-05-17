import numpy as np
import copy
import svgwrite
from math import degrees, radians, cos, sin
import random

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

def lineseg_intersect(l1, l2):
    d = (l2.y2 - l2.y1) * (l1.x2 - l1.x1) - (l2.x2 - l2.x1) * (l1.y2 - l1.y1)
    if d == 0: #rovnobezky
        return False
    n_a = (l2.x2 - l2.x1) * (l1.y1 - l2.y1) - (l2.y2 - l2.y1) * (l1.x1 - l2.x1)
    n_b = (l1.x2 - l1.x1) * (l1.y1 - l2.y1) - (l1.y2 - l1.y1) * (l1.x1 - l2.x1)
    
    u_a = n_a / float(d)
    u_b = n_b / float(d)
    if 0 <= u_a <= 1 and 0 <= u_b <= 1:
        x = l1.x1 + (u_a * (l1.x2 - l1.x1))
        y = l1.y1 + (u_a * (l1.y2 - l1.y1))
        return (x,y)
    else:#prunik mimo usecky
        return False

def p_dist(p1, p2):
        a = (p1[0] - p2[0]) ** 2
        b = (p1[1] - p2[1]) ** 2
        return (a + b) ** 0.5


def same_point(p1,p2,acc=0.000001):
    if (p1[0]-acc) <= p2[0] <= (p1[0]-acc) and (p1[1]-acc) <= p2[1] <= (p1[1]-acc):
        return True
    return False

def rand_second_point(point, distance):
    x_dist = random.uniform(-distance, distance)
    y_dist = random.choice([-1,1]) * (distance**2 - x_dist**2)**0.5
    return point[0]+x_dist, point[1]+y_dist 

def random_linesegments(ammount,distance, maxi=None):
    if not maxi:
        maxi = distance*10
    
    linesegments = []
    for _ in range(ammount):
        x1 = random.uniform(0, maxi)
        y1 = random.uniform(0, maxi)
        
        p2 = rand_second_point((x1,y1), distance)
        lineseg = Line((x1,y1),p2)
        
        linesegments.append(lineseg)
    return linesegments


def points_from_linesegments(lsegs):
    points = reduce(lambda x,y: x.add(y.p1) or x.add(y.p2) or x, lsegs, set())
    return points


def triangulate(points):
#    print points
    linesegs = set() # lines triangulation consists of
    usedpoints = set() # processed poitns
    
    for p in points:
#        print "!!!!!!\n",p
        # add all possible lines which don't break triangulation
        for p2 in sorted(list(usedpoints)):
#            print 'p2', p2
            l = Line(p, p2)
            nointersects = True
            for iline in linesegs:
                if l.p2 == iline.p1 or l.p2 == iline.p2 or \
                    l.p1 == iline.p1 or l.p1 == iline.p2:
                    continue
                inters = lineseg_intersect(l, iline)
#                print inters
                if inters:
                    nointersects = False
                    break
            if nointersects:
#                print 'added'
                linesegs.add(l)
        usedpoints.add(p)
    return linesegs

if __name__ == '__main__':
    dwg = svgwrite.Drawing('triangulation.svg')
    offset = 200
    
    lsegs = random_linesegments(200, 60)
    pts = points_from_linesegments(lsegs)
    
    pts = list(pts)
    p0 = pts[0]
    pts.sort(key=lambda x: p_dist(p0, x))
    
    for p in pts:
        dwg.add(dwg.circle((p[0]+offset,p[1]+offset),r=1, stroke=svgwrite.rgb(255, 0, 0, '%')))
    lines = triangulate(pts)
    for l in lines:
        l.to_svg(dwg,offset)
    dwg.save()
    
