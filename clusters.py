
import sys, svgwrite

def load_point_file(fname):
    with open(fname, 'r') as fp:
        xys = []
        for row in fp:
            lst = row.split()
            lst = map(float, lst)
            xys.append(lst)
    return xys


def p_dist(p1, p2):
    a = (p1[0] - p2[0]) ** 2
    b = (p1[1] - p2[1]) ** 2
    return (a + b) ** 0.5


def clusters(points):
    alldistsd = {}
    sumdistsd = {}
    prvni = points[0]
    
    movingpoints = map(lambda a: (a,a,1), points)
    
    for p1 in points:
        distsl = []
        sumd = 0
        
        newp = p1
        
        for p2 in points:
            if p1 == p2:
                continue
            dist = p_dist(p1,p2)
            distsl.append((dist**2, p2))
        
        distsl.sort(key=lambda a:a[0])
        
        # soucet gravitacnich sil jakymi bod pusobi na ostatni, 3 extremy vyradim
#        sumd = reduce(lambda p, nxt: p+1.0/nxt[0], distsl[3:-3], 0)
        sumd = reduce(lambda p, nxt: p+1.0/nxt[0], distsl, 0)
        
        if p1 == prvni:
            print distsl
        
        alldistsd[p1] = distsl
        sumdistsd[p1] = sumd
    return alldistsd, sumdistsd
    


if __name__ == '__main__':
    
    
    points = map(tuple, load_point_file(sys.argv[1]))
    
    #normalization of points
    minx = min(points,key=lambda x: x[0])[0]
    miny = min(points,key=lambda x: x[1])[1]
    points = map(lambda a: (a[0]-minx, a[1]-miny), points)
    
    maxx = max(points,key=lambda x: x[0])[0]
    maxx = max(points,key=lambda x: x[1])[1]
    
    
    
    
    dwg = svgwrite.Drawing(sys.argv[1]+'.svg')
    
    for i in points:
        dwg.add(dwg.circle((i[0]*10,i[1]*10),r=1, stroke=svgwrite.rgb(255, 0, 0, '%')))
    
    
    
    
    alldistsd, sumdistsd = clusters(points)
    
    smallestp = sorted(sumdistsd.items(), key=lambda (k,v): (v,k), reverse=True)
    
    print '\n\n\n\n', smallestp
    for p in smallestp[:5]:
        i = p[0]
        dwg.add(dwg.circle((i[0]*10,i[1]*10),r=1.5, stroke=svgwrite.rgb(0, 0, 255, '%')))
    
    dwg.save()
    