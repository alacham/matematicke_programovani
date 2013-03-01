import random
import time
import math

def montecarlo_pi(nsamples):
    cntr = 0
    for _ in range(nsamples):
        x, y = random.uniform(0,1), random.uniform(0,1)
        if (x*x + y*y) <= 1:
            cntr += 1
    return cntr / (nsamples * 0.25) 

# za vetrinu +- 540 000 vzroku, chyba az asi 2 tisiciny
def montecarlo_pi_timed(timelim=1):
    started = time.time()
    cntr = 0
    nthousands = 0
    # myslim, ze time() vyrizuje kernel > pomale, volam jednou za cas
    while (time.time() - started) < 1:
        nthousands += 1
        for _ in xrange(1000):
            x, y = random.uniform(0,1), random.uniform(0,1)
            if (x*x + y*y) <= 1:
                cntr += 1
    
    ap_pi = cntr / (nthousands * 250.0)
    print nthousands*1000, 'vzorku; rozdil:', abs(ap_pi-math.pi)
    return ap_pi 

print montecarlo_pi_timed(1)

# zdesetinasobeni iteraci prida +- 1 desetinne cislo
def gregory_liebniz_pi(nsteps=1000):
    summed = 4
    divider = 1.0
    sign = 4.0
    for _ in xrange(nsteps):
        sign *= -1.0
        divider += 2.0
        summed += sign/divider
    return summed

def gregory_liebniz_pi_timed(timelim=1):
    started = time.time()
    summed = 4
    divider = 1.0
    sign = 4.0
    nthousands = 0
    while (time.time() - started) < 1:
        nthousands += 1
        for _ in xrange(1000):
            sign *= -1.0
            divider += 2.0
            summed += sign/divider
    print nthousands*1000, 'vzorku; rozdil:', abs(summed-math.pi)
    return summed

print gregory_liebniz_pi_timed(1)

#udajne by 10 iteracemi melo zvysit presnos o 3 desetinna cisla,
# vychazi mi o neco min; uz pri nsteps=200 narazim na float NaN
# kazdopadne mnohem rychlejsi nez predchozi...
def arctan_pi(nsteps=150):
    started = time.time()
    summed = 2
    multall = 2.0
    multodd = 1.0
    odds = 1.0
    for i in xrange(1,nsteps+1):
        odds += 2
        multall *= i
        multodd *= odds
        summed += multall/multodd
    print "%d kroku; rozdil: %e, behem: %f(s)" % (nsteps, abs(summed-math.pi),
                                                   time.time()-started)
    return summed

print arctan_pi(150)
