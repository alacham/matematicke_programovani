from myturtle import *

tree_lsys_translations = {'I': [[Turtle.pos_push], [Turtle.left, 45]],
                          'R': [[Turtle.pos_pop], [Turtle.right, 45]],
                          'S': [[Turtle.forward, 10]],
                          'L': [[Turtle.forward, 10]]}

tree_recipe = lsys_rewrite({'L':'SILRL', 'S':'SS'}, 'L', 6)


a = Turtle(0, 0)

DRAWIMAGE = 1

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
    pass


a.draw()
