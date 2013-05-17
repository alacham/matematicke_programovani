import sys
import Queue


# node ... (y,x)
# edge ... (node1, node2, cost)

EMPTY = '.'
WALL = '#'
PATH = 'x'
START = 'S'
END = 'E'
DYNAMITE = '!'


INF = float('inf') 

def dynamite_add_edge(maze, nodes_edg, cnode, dyncost=1000):
    ct = maze[cnode[0]][cnode[1]]
    if ct == END:
        return
    
    hei_maze = len(maze)
    wid_maze = len(maze[0])
    
    
    nodes_edg[cnode] = nodes_edg.get(cnode,{})
    cndict = nodes_edg[cnode]
    
    for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
        nextnode = (cnode[0]+dy , cnode[1]+dx)
        if not ( 0 <= nextnode[0] < hei_maze) or not ( 0 <= nextnode[1] < wid_maze):
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
    
    dcost = len(maze)*len(maze[0])
    
    endnode = (0,0)
    
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == START:
                startnode = (y,x)
            elif maze[y][x] == END:
                endnode = (y,x)
            
            dynamite_add_edge(maze, nodes_edges, (y,x), dcost)
    
    return maze, nodes_edges, startnode,  endnode


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



if __name__ == '__main__':
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
