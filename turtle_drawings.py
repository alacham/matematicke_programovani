from math import degrees, atan, e
from myturtle import *


tree_lsys_translations = {'I': [[Turtle.pos_push], [Turtle.left, 45]],
                          'R': [[Turtle.pos_pop], [Turtle.right, 45]],
                          'S': [[Turtle.forward, 10]],
                          'L': [[Turtle.forward, 10]]}

tree_recipe = lsys_rewrite({'L':'SILRL', 'S':'SS'}, 'L', 6)

koch_recipe = lsys_rewrite({'S':'SLSRSLS'}, 'SRSRS', 3)
koch_lsys_translation = {'S': [[Turtle.forward, 10]],
                         'L': [[Turtle.left, 60]],
                         'R': [[Turtle.right, 120]]}

serpinsky_recipe = lsys_rewrite({'S':'FLSLF', 'F':'SRFRS'}, 'S', 7)
serpinsky_lsys_translation = {'S': [[Turtle.forward, 1.2]],
                              'F': [[Turtle.forward, 1.2]],
                              'L': [[Turtle.left, 60]],
                              'R': [[Turtle.right, 60]]}

hilbert_recipe = lsys_rewrite({'1':'L2FR1F1RF2L',
                               '2':'R1FL2F2LF1R'}, '1', 6)
hilbert_lsys_translation = {'F': [[Turtle.forward, 3]],
                            'L': [[Turtle.left, 87]],
                            'R': [[Turtle.right, 87]]}

a = Turtle(0, 0)

DRAWIMAGE = 6

if DRAWIMAGE == 1:
    a.nuhelnik(10, 100)
    a.forward(100)
    
    ## pentagram v 5 uhelniku
    a.nuhelnik(5, 50)
    a.left(36)
    a.pentagram(50 * ((1 + (5 ** 0.5)) / 2))
    
    a.forward(150)
    a.hvezda(12, 150)
    a.right(160)
    print tree_recipe
    a.lsys_interpret(tree_recipe, tree_lsys_translations)
elif DRAWIMAGE == 2:
    # pomer zlateho rezu
    #kratsi = 2
    #delsi = (1 + (5 ** 0.5))
    
    # pomer 1 : e
    kratsi = 1
    delsi = e
    edge_len = 300.0
    turn = degrees(atan(kratsi / delsi))
    multip = (((kratsi ** 2) + delsi ** 2) ** 0.5) / (kratsi + delsi)
    while edge_len >= 2:
        for _ in xrange(4):
            a.forward(edge_len)
            a.right(90)
        a.forward(edge_len * (kratsi / (kratsi + delsi)))
        a.right(turn)
        edge_len *= multip
elif DRAWIMAGE == 3:
    spacesize = 5
    edge_len = 1
    a.offset = 200
    a.right(150)
    a.pen_down()
    while edge_len < 350:
        for _ in xrange(3):
            a.forward(edge_len)
            a.right(120)
        a.left(150)
        a.pen_up()
        a.forward(spacesize+0.5)
        a.pen_down()
        a.right(150)
        edge_len += 2 * spacesize
elif DRAWIMAGE == 4:
    a.offset = 300
    a.lsys_interpret(koch_recipe, koch_lsys_translation)
elif DRAWIMAGE == 5:
    a.offset = 20
    a.lsys_interpret(serpinsky_recipe, serpinsky_lsys_translation)
elif DRAWIMAGE == 6:
    a.offset = 1
    a.lsys_interpret(hilbert_recipe, hilbert_lsys_translation)

a.draw()
