from PIL import Image
import colorsys

def nsd_mod(a, b, nth):
    if b == 0:
        return a, nth
    else:
        return nsd_mod(b, a % b, nth + 1)


def nsd_minus(a, b, *args):
    if a == 0:
        return b, 0
    i = 0
    while b != 0:
        i += 1
        if a > b:
            a = a - b
        else:
            b = b - a
    return a, i


def euclid_show(size, mode):
    im = Image.new("RGB", (size, size+10))
    pix = im.load()
    
    # 0.9 because in sRGB spectrum I prefer (red to violet) to (red to red)
    size_step = 0.9/(size-1)
    for x in range(0,size):
            hsv_colors = (x*size_step, 1, 1)
            rgb_colors = colorsys.hsv_to_rgb(*hsv_colors)
            INT_RGB = float2int_colors(rgb_colors)
            for y in range(size+2,size+10):
                pix[x,y] = INT_RGB
    
    bigarr = []
    max_mod = 0
    max_minus = 0
    for y in xrange(0, size):
        subarr = []
        for x in xrange(0, size):
            mod_n = nsd_mod(x, y, 0)[1]
            minus_n = nsd_minus(x, y, 0)[1] 
            max_mod = max(max_mod, mod_n)
            max_minus = max(max_minus, minus_n)
            
            subarr.append((minus_n, mod_n))
        bigarr.append(subarr)
    
    mod_step = 0.9 / max_mod
    minus_step = 0.9 / max_minus
    
    for y in xrange(0, size):
        for x in xrange(0, size):
            if mode == 1 or mode == 2:
                if mode == 1:
                    step = minus_step
                    i = 0
                else:
                    step = mod_step
                    i = 1
                hsv_colors = (bigarr[y][x][i] * step, 1, 1) 
                rgb_colors = colorsys.hsv_to_rgb(*hsv_colors)
            else:
                h = bigarr[y][x][1] * mod_step
                # value will be from 0.3 to 1
                v = (7.0/9) * bigarr[y][x][0] * minus_step + 0.3
                hsv_colors = (h, 1, v) 
                rgb_colors = colorsys.hsv_to_rgb(*hsv_colors)
            pix[x, size - y - 1] = float2int_colors(rgb_colors)
    im.show()



def draw_rainbow():
    im = Image.new("RGB", (256, 20))
    step = 1.0/255
    for x in range(0,256):
        for y in range(0,20):
            im.putpixel((x,y),float2int_colors(colorsys.hsv_to_rgb(x*step,1,1)))
    im.show()


def float2int_colors(float_cols):
    return tuple(map(lambda a: int(round(255 * a)), float_cols))

if __name__ == "__main__":
#    draw_rainbow()
    size = input("Size(axis len): ")
    mode = input("Minus(1),Mod(2),Both(3): ")
    euclid_show(size, mode)
