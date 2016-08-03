import heapq
import math
import random
grid_map=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 1, 1, 0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 1, 1, 1, 0], [0, 0, 1, 1, 0, 1, 1, 0, 1, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]]
def solve(start, finish, heuristic):
    """Find the shortest path from START to FINISH."""
    heap = []

    link = {} # parent node link
    h = {} # heuristic function cache
    g = {} # shortest path to a node

    g[start] = 0
    h[start] = 0
    link[start] = None


    heapq.heappush(heap, (0, start))
    # keep a count of the  number of steps, and avoid an infinite loop.
    while True:
        
        
        f, current = heapq.heappop(heap)
        #print current
        if current == finish:
            print "distance:", g[current]
            return g[current], build_path(start, finish, link)
        
        moves = current.get_moves()
        distance = g[current]
        for mv in moves:
            print mv.x,mv.y
            if grid_map[mv.x][mv.y]==1 or mv.x==0 or mv.y==0:
                continue
                
            if  (mv not in g or g[mv] > distance + 1):
                g[mv] = distance + 1
                if  mv not in h:
                    h[mv] = heuristic(mv)
                link[mv] = current
                heapq.heappush(heap, (g[mv] + h[mv], mv))
    else:
        raise Exception("did not find a solution")

def build_path(start, finish, parent):
    """
    Reconstruct the path from start to finish given
    a dict of parent links.

    """
    x = finish
    xs = [x]
    while x != start:
        x = parent[x]
        xs.append(x)
    xs.reverse()
    print xs
    return xs

def no_heuristic(*args):
   """Dummy heuristic that doesn't do anything"""
   return 0

class GridPosition(object):
    """Represent a position on a grid."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return "GridPosition(%d,%d)" % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_moves(self):
        #print "coordiantes",self.x, self.y
        #print self.x,self.y
        #if grid_map[self.x][self.y]!=1:
        # There are times when returning this in a shuffled order
        # would help avoid degenerate cases.  For learning, though,
        # life is easier if the algorithm behaves predictably.
        if self.x>=0 and self.x<=len(grid_map)-1 and self.y>=0 and self.y<=len(grid_map)-1:
            if self.x + 1<len(grid_map):
                yield GridPosition(self.x + 1, self.y)
            if self.y + 1<len(grid_map):  
                yield GridPosition(self.x, self.y + 1)
            if self.x - 1>=-1:
                yield GridPosition(self.x - 1, self.y)
            if self.y - 1>=-1:
                yield GridPosition(self.x, self.y - 1)
                
def manhattan_h(goal):
   def f(pos):
       dx, dy = pos.x - goal.x, pos.y - goal.y
       return abs(dx) + abs(dy)
   return f

def grid_test_manhattan_heuristic():
    solve(grid_start, grid_end, manhattan_h(grid_end))

   
   
grid_start = GridPosition(8,8)
grid_end = GridPosition(4,1)
grid_test_manhattan_heuristic()
