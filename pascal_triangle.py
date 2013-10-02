
from euclid_alg import float2int_colors
import colorsys, Image

def pascal_triangle(lnum=15):
    rows = [[1]]
    lnum = max(1, lnum - 1)
    for i in xrange(lnum):
        rows.append(next_pascal_row(rows[-1]))
    return rows

def next_pascal_row(previous):
    new = []
    delka = len(previous)
    new.append(1)
    for i in xrange(delka - 1):
        new.append(previous[i] + previous[i + 1])
    new.append(1)
    return new


def draw_colored_square(pixmap, position, coltuple, size=4):
    sx, sy = position
    for x in xrange(size):
        for y in xrange(size):
            pixmap[sx + x, sy + y] = coltuple

def draw_colored_pascal_triangle(rownum, moduloclass=5, squaresize=4):
    triang = pascal_triangle(rownum)
    colstep = 0.9 / (moduloclass - 1)
    mycolors = [None for i in xrange(moduloclass)]
    #kazde zbytkove tride prirad barvu
    for i in range(moduloclass):
        hsv_colors = (i * colstep, 0.8, 0.8)
        mycolors[i] = float2int_colors(colorsys.hsv_to_rgb(*hsv_colors))
    
    imsize = squaresize * rownum
    im = Image.new("RGB", (imsize, imsize))
    pix = im.load()
    startx = (imsize / 2) - (squaresize / 2)
    y = 0
    for row in triang:
        x = startx
        for num in row:
            mc = num % moduloclass
            draw_colored_square(pix, (x, y), mycolors[mc], squaresize)
            x += squaresize 
        y += squaresize
        startx -= squaresize / 2
    im.show()
    
    
def draw_colored_pascal_triangle2(rownum, moduloclass=5, squaresize=4):
    triang = pascal_triangle(rownum)
    colstep = 0.9 / (moduloclass - 1)
    mycolors = [None for i in xrange(moduloclass)]
    #kazde zbytkove tride prirad barvu
    for i in range(moduloclass):
        hsv_colors = (i * colstep, 0.8, 0.8)
        mycolors[i] = float2int_colors(colorsys.hsv_to_rgb(*hsv_colors))
    
    imsize = squaresize * rownum
    im = Image.new("RGB", (imsize, imsize))
    pix = im.load()
    startx = (imsize / 2) - (squaresize / 2)
    y = 0
    for row in triang:
        x = startx
        for num in row:
            mc = num % moduloclass
            if mc == 1:
                draw_colored_square(pix, (x, y),(255,255,255) , squaresize)
            else:
                draw_colored_square(pix, (x, y), (0,0,0), squaresize)
            x += squaresize 
        y += squaresize
        startx -= squaresize / 2
    im.show()

if __name__ == '__main__':
#    

    draw_colored_pascal_triangle2(80, 5, 8)
    

