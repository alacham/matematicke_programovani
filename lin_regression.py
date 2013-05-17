

import sys, math

with open(sys.argv[1], 'r') as fp:
    points = []
    for row in fp:
        d = {}
        x, y = row.split()
        d['x'] = float(x)
        d['y'] = float(y)
        points.append(d)



def lin_regres(indicts):
    va = 'x'
    vb = 'y'
    nm = len(indicts)
    valsa = map(lambda a: a[va], indicts)
    valsb = map(lambda a: a[vb], indicts)
    valsab = zip(valsa, valsb)
    nm = len(valsab)
    avga = sum(valsa)/float(nm)
    avgb = sum(valsb)/float(nm)
    
    deviation2a = sum(map(lambda a: (a-avga)**2, valsa))/nm
    deva = deviation2a ** 0.5
    deviation2b = sum(map(lambda a: (a-avgb)**2, valsb))/nm
    devb = deviation2b ** 0.5

    pearsq = sum(map(lambda a: ((a[0]-avga)/deva)*((a[1]-avgb)/deva),valsab ))/nm
    print 'PearsKoeficient:', pearsq

    kovar = sum(map(lambda a: a[0]*a[1],valsab ))/nm - avga*avgb
    koef = kovar/deviation2a
    
    print 'Regresni primka y = %f + %f x' % (avgb-koef*avga, koef)
    
lin_regres(points)