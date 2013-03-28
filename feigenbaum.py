import Image

def feigenbaum(r, nsteps=500, ntrash=100, init=0.5):
    vals = []
    if 0 <= init <= 1:
        x = init
    else:
        x = 0.5
    for i in range(nsteps):
        x = 4 * r * x * (1 - x)
        if i >= ntrash:
            vals.append(x)
    return vals


def feigenbaum_visual(rb=(0, 1), valb=(0, 1), imsize=(256, 256), name='feigenbaum.png'):
    im = Image.new("RGB", imsize)
    
    rstep = (rb[1] - rb[0]) / float(imsize[0])# without upper bound
    
    vmult = float(imsize[1]) / (valb[1] - valb[0])
    
    r = rb[0]
    for x in range(imsize[0]):
        vals = feigenbaum(r)
        print r
        print vals
        for v in vals:
            if not (valb[0] <= v <= valb[1]):
                continue            
            yv = int(round((v - valb[0]) * vmult))
            im.putpixel((x, 255 - yv), (255, 255, 255))
        r += rstep
    im.save(name)


#print feigenbaum(1.0, 200, ntrash=0, init=0.5) 

feigenbaum_visual(rb=(0.85, 0.9), valb=(0.8, 0.9))
