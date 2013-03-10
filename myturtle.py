from math import sin, cos, radians
import svgwrite

def lsys_rewrite(r_rules, initial, count):
    if count > 0:
        rewritten = reduce(lambda x, y:x + r_rules.get(y, y), initial, "")
        return lsys_rewrite(r_rules, rewritten, count - 1)
    else:
        return initial

class Turtle:
    def __init__(self, x, y, outfilename='test.svg'):
        self.x = 0
        self.y = 0
        self.pen = True
        self.position_stack = []
        self.angle = 0
        self.offset = 500
        self.dwg = svgwrite.Drawing(outfilename)#, profile='tiny')
        #self.dwg.add(self.dwg.line((0, 0), (1, 1), stroke=svgwrite.rgb(10, 10, 16, '%')))
        #self.dwg.add(self.dwg.line((1000, 1000), (999, 999), stroke=svgwrite.rgb(10, 10, 16, '%')))
    
    def right(self, ang):
        self.angle -= ang
    
    def left(self, ang):
        self.angle += ang
    
    def draw(self):
        self.dwg.save()
    
    def forward(self, howmuch):
        y = self.y + cos(radians(self.angle)) * howmuch
        x = self.x + sin(radians(self.angle)) * howmuch
        if self.pen:
            #self.dwg.add(self.dwg.line((int(self.x + self.offset), int(self.y + self.offset)), (int(x + self.offset), int(y + self.offset)), stroke=svgwrite.rgb(10, 10, 16, '%')))
            self.dwg.add(self.dwg.line((self.x + self.offset, self.y + self.offset), (x + self.offset, (y + self.offset)), stroke=svgwrite.rgb(10, 10, 16, '%')))
        self.x = x
        self.y = y
        #print x, y
    
    def pen_down(self):
        self.pen = True
    
    def pen_up(self):
        self.pen = False
    
    def backward(self, howmuch):
        self.forward(-howmuch)
    
    def hvezda(self, n, delkastrany):
        stredovy = 360.0 / n
        zatacka = 180 - stredovy
        for _ in xrange(n):
            self.forward(delkastrany)
            self.left(zatacka)
    
    def pentagram(self, delkastrany):
        self.hvezda(10, delkastrany)
    
    def nuhelnik(self, n, delkastrany):
        uhel = 360.0 / n
        for _ in xrange(n):
            self.forward(delkastrany)
            self.left(uhel)
    
    def pos_push(self):
        state = (self.x, self.y, self.angle, self.pen)
        self.position_stack.append(state)
    
    def pos_pop(self):
        state = self.position_stack.pop()
        self.x, self.y, self.angle, self.pen = state
        
    def lsys_interpret(self, recipe, translation):
        for symbol in recipe:
            actions = translation.get(symbol, [])
            for action in actions:
                action[0](self, *action[1:])

