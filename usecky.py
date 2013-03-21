import svgwrite
from math import degrees, atan, e, pi
import random

class Usecka:
    
    def __init__(self, p1, p2):
        self.x1, self.y1 = p1
        self.x2, self.y2 = p2
        self.p1 = p1
        self.p2 = p2
    
    def to_svg(self,svgdwg, offset):
        dwg = svgdwg
        dwg.add(dwg.line((self.x1 + offset, self.y1 + offset), (self.x2 + offset, self.y2 + offset), stroke=svgwrite.rgb(10, 10, 16, '%')))
    


def prunik_usecek(l1, l2):
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
        lineseg = Usecka((x1,y1),p2)
        
        linesegments.append(lineseg)
    return linesegments
        

def draw_linesegs(linesegs, outname, offset=100):
    dwg = svgwrite.Drawing(outname)
    
    for line in linesegs:
        line.to_svg(dwg,offset)
    
    #intersections
    intersections = []
    for l1 in range(len(linesegs)):
        line1 = linesegs[l1]
        for l2 in range(l1+1, len(linesegs)):
            line2 = linesegs[l2]
            
            intersection = prunik_usecek(line1, line2)
            if intersection:
                intersections.append(intersection)
    
    for i in intersections:
        dwg.add(dwg.circle((i[0]+offset,i[1]+offset),r=1, stroke=svgwrite.rgb(255, 0, 0, '%')))
        
    dwg.save()
    

lsegs = random_linesegments(500, 100)
draw_linesegs(lsegs,  'randlinesegs.svg', 100)



    
    