import sys
import Queue
import random
import svgwrite
import transformace



class Wall(transformace.Line):
    def switch_xy(self):
        x, y = self.x1, self.y1
        self.x1, self.y1 = y, x
        x, y = self.x2, self.y2
        self.x2, self.y2 = y, x

# node ... (y,x)
# edge ... (node1, node2, cost)

EMPTY = '.'
WALL = '#'
PATH = 'x'
START = 'S'
END = 'E'
DYNAMITE = '!'


INF = float('inf') 



def modify_coords(tochng):
    mult = 2
    outs = []
    for i in tochng:
        if isinstance(i, tuple):
            outs.append(modify_coords(i))
        else:
            outs.append(1 + i * mult)
    return tuple(outs)



def dynamite_add_edge(maze, nodes_edg, cnode, dyncost=1000):
    ct = maze[cnode[0]][cnode[1]]
    if ct == END:
        return
    
    hei_maze = len(maze)
    wid_maze = len(maze[0])
    
    
    nodes_edg[cnode] = nodes_edg.get(cnode, {})
    cndict = nodes_edg[cnode]
    
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nextnode = (cnode[0] + dy , cnode[1] + dx)
        if not (0 <= nextnode[0] < hei_maze) or not (0 <= nextnode[1] < wid_maze):
            continue
        
        nt = maze[nextnode[0]][nextnode[1]]
        if nt == WALL:
            cndict[nextnode] = dyncost
        else:
            cndict[nextnode] = 1


def load_dynamite_maze(fname):
    nodes_edges = dict()
    maze = []
    with open(fname) as f:
        for line in f:
            maze.append(line.strip())
    
    dcost = len(maze) * len(maze[0])
    
    endnode = (0, 0)
    
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == START:
                startnode = (y, x)
            elif maze[y][x] == END:
                endnode = (y, x)
            
            dynamite_add_edge(maze, nodes_edges, (y, x), dcost)
    
    return maze, nodes_edges, startnode, endnode


def djikstra(neighbours, startnode, endnode):
    nodecosts = {startnode : 0}
    prevonpath = {startnode : None}
    que = Queue.PriorityQueue()
    que.put((0, startnode))
    try:
        while True:
            curcost, curnode = que.get_nowait()
            if curnode == endnode:
                break
            for tonode, edgecost in neighbours[curnode].iteritems():
                cost = nodecosts.get(tonode, INF)
                if cost > (curcost + edgecost):
                    nodecosts[tonode] = curcost + edgecost
                    prevonpath[tonode] = curnode
                    que.put((curcost + edgecost, tonode))
    except Queue.Empty:
        print "There is no way to endnode"
        sys.exit(0)
        
    return prevonpath, nodecosts



def basic_maze(height, width, sy, sx):
    edges = {}
    
    def randomized_dfs(pos):
        y, x = pos
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(dirs)
        
        for dy, dx in dirs:
            ny, nx = y + dy, x + dx 
            
            if not (0 <= ny < height) or not (0 <= nx < width):
                continue
            
            if (ny, nx) in edges:
                continue
            
            edges[pos] = edges.get(pos, {})
            edges[pos][ny, nx] = 1
            edges[(ny, nx)] = edges.get((ny, nx), {})
            edges[ny, nx][pos] = 1
            randomized_dfs((ny, nx))
            
    randomized_dfs((sy, sx))
    
    destroywalls = set()
    for k, v in edges.iteritems():
        for kk, _ in v.iteritems():
            destroywalls.add((k, kk))
    
    maze = []
    for row in range(height):
        maze.append(['+', '--'] * width + ['+'])
        maze.append(['|', '  '] * width + ['|'])
    maze.append(['+', '--'] * width + ['+'])
    
    for p1, p2 in modify_coords(destroywalls):
        y1, x1 = p1
        y2, x2 = p2
        maze[(y1 + y2) / 2][(x1 + x2) / 2] = [' ', '  '][abs(y1 - y2) / 2]
    for row in maze:
        print ''.join(row)
    
    
    
def init_djikstra():
    maze, neighbours, start, end = load_dynamite_maze(sys.argv[1])
    prevs, costs = djikstra(neighbours, start, end)
    
    charmaze = [ [ char for char in line ] for line in maze ]
    cnode = prevs[end]
    while cnode != start:
        y, x = cnode
        if charmaze[y][x] == WALL:
            charmaze[y][x] = DYNAMITE
        elif charmaze[y][x] == EMPTY:
            charmaze[y][x] = PATH
        cnode = prevs[cnode]
    
    for charlist in charmaze:
        print ''.join(charlist)

def triangle_maze(size):
    walls_d = {}
    walls_all = set()
    
    for i in range(1, size):
        for j in range(i + 1):
            #down
            if j >= 1:
                walls_d[((i, j * 2 - 1), (i, j * 2))] = Wall((i, j), (i + 1, j))
                walls_all.add(((i, j * 2 - 1), (i, j * 2)))
            #horizontal
            if j < i :
                walls_d[((i - 1, j*2), (i, j*2 + 1))] = Wall((i, j), (i, j + 1))
                walls_all.add(((i - 1, j*2), (i, j*2 + 1)))                
                #diagonal
                walls_d[((i, j * 2), (i, j * 2 + 1))] = Wall((i, j), (i + 1, j + 1))
                walls_all.add(((i, j * 2), (i, j * 2 + 1)))
    #outer walls
    walls_d[((-10, -10), (-10, -10))] = Wall((0, 0), (size, 0))
    walls_all.add(((-10, -10), (-10, -10)))
    walls_d[((-11, -11), (-11, -11))] = Wall((size, 0), (size, size))
    walls_all.add(((-11, -11), (-11, -11)))
    walls_d[((-12, -12), (-12, -12))] = Wall((size, size), (0, 0))
    walls_all.add(((-12, -12), (-12, -12)))
    
    def get_neighs(pos):
        y, x = pos
        neighs = []
        if x % 2 == 0:
            for dy, dx in [(0, -1), (0, 1), (1, 1)]:
                ny, nx = y + dy, x + dx
                if nx > 2 * ny or nx < 0 or ny >= size:
                    continue
                neighs.append((ny, nx))
        else:
            for dy, dx in [(-1, -1), (0, 1), (0, -1)]:
                ny, nx = y + dy, x + dx
                if nx > 2 * ny or nx < 0 or ny >= size or ny < 0:
                    continue
                neighs.append((ny, nx))
        return neighs
    
    
    edges = {}
    
    def randomized_dfs(pos):
        neighs = get_neighs(pos)
        random.shuffle(neighs)
        for ny, nx in neighs:
            if (ny, nx) in edges:
                continue
            edges[pos] = edges.get(pos, {})
            edges[pos][ny, nx] = 1
            edges[(ny, nx)] = edges.get((ny, nx), {})
            edges[ny, nx][pos] = 1
            randomized_dfs((ny, nx))
    
    randomized_dfs((0, 0))
    
    destroywalls = set()
    for k, v in edges.iteritems():
        for kk, _ in v.iteritems():
            destroywalls.add((k, kk))
    
    walls_rest = walls_all.difference(destroywalls)
    
    dwg = svgwrite.Drawing('results/triangle_maze.svg')
    for w in walls_rest:
        wall = walls_d[w]
        #wall.switch_xy()
        wall.apply_transform(transformace.scaleMatrix(14, 10))
        wall.apply_transform(transformace.shearMatrix(-0.7))
        wall.to_svg(dwg, 0)

    dwg.save()



if __name__ == '__main__':
    init_djikstra()
    basic_maze(30, 40, 0, 0)
    triangle_maze(40)
