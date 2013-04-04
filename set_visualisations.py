import Image
from chaos_game import ir



def newton_z3(starting,diff=0.0001):
    
    def i_konv_diff(num, diff):
        z = (3**0.5)/2
        if abs(num - complex(1,0)) < diff:
            return True, 1
        if abs(num - complex(-0.5,z)) < diff:
            return True, 2
        if abs(num - complex(-0.5,-z)) < diff:
            return True, 3
        else:
            return False, 0
    
    x = starting
    step = 0
    while True:        
        res = i_konv_diff(x, diff)
        if res[0]:
            break
        step += 1
        x = x - ((x**3 - 1)/ (3 * x**2))
    return res[1], step


def mandelbrot(const,nsteps=64):
    visited = set()
    visited.add(0)
    x = 0
#    flag = False
#    step = 0
    for i in range(nsteps):
        x = x**2 + const
        if x in visited:
            return (True, i)
        if abs(x) > 2: # move outta loop?
            return (False, i)
        visited.add(x)
    return (True, nsteps)


def julius(starting, const, nsteps=64):
    visited = set()
    visited.add(starting)
    x = starting
#    flag = False
#    step = 0
    for i in range(nsteps):
        x = x**2 + const
        if x in visited:
            return (True, i)
        if abs(x) > 2: # move outta loop?
            return (False, i)
        visited.add(x)
    return (True, nsteps)


def make_2arr(realrng, irng, realstep, istep, function, funargs):
    mand2arr = []
    
    curi = irng[0]
    while curi < irng[1]:
        currow = []
        curreal = realrng[0]
        while curreal < realrng[1]:
            currow.append(function(complex(curreal,curi),*funargs))
            curreal += realstep
            
        mand2arr.append(currow)
        curi += istep
    return mand2arr

def plot_2arr(arr2, name='mandelbrot.png', ndiv=64):
    imsize = (len(arr2[0]),len(arr2))
    im = Image.new("RGB", imsize)
    
    for y in range(imsize[1]):
        for x in range(imsize[0]):
            ins, steps = arr2[y][x]
            if ins:
                im.putpixel((x, (imsize[1]-1) - y), (255, 255, ir((255.0/ndiv) * steps)))
            else:
                im.putpixel((x, (imsize[1]-1) - y), (2*ir((255.0/ndiv) * steps), 0, 0))
    
    im.save(name)
    
if __name__ == '__main__':
    #m2arr = make_2arr((-2,1), (-1.2,1.2), 0.005, 0.005, mandelbrot, [])
    #plot_2arr(m2arr, 'mandl1.png')
    
    #m2arr = make_2arr((-2,2), (-2,2), 0.01, 0.01, julius, [complex((2**0.5)/3, (2**0.5)/3)])
    
    #m2arr = make_2arr((-2,2), (-2,2), 0.01, 0.01, julius, [-complex((2**0.5)/3, (2**0.5)/3)])
    
    m2arr = make_2arr((-2,2), (-2,2), 0.01, 0.01, julius, [complex(-(2**0.5)/3, (2**0.5)/3)])
    plot_2arr(m2arr, 'jul1.png')