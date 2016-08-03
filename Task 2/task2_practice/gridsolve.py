import heapq
grid_map=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 1, 1, 0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 1, 1, 1, 0], [0, 0, 1, 1, 0, 1, 1, 0, 1, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]]
cost=[0]


def search(x, y,k,l):
    
  
    visited=set()
    if x==k and y==l:
        print 'found at %d,%d' % (x, y)
        return True
    elif grid_map[x][y] == 1:
        print 'wall at %d,%d' % (x, y)
        return False
    elif grid_map[x][y] == 3:
        print 'visited at %d,%d' % (x, y)
        return False

    print 'visiting %d,%d' % (x, y)
    # mark as visited
    grid_map[x][y] = 3

    # explore neighbors clockwise starting by the one on the right
    if ((x < len(grid_map)-1 and search(x+1, y,k,l))
        or (y > 0 and search(x, y-1,k,l))
        or (x > 0 and search(x-1, y,k,l))
        or (y < len(grid_map)-1 and search(x, y+1,k,l))):
        return True

    return False

search(4, 4,8,8)
print "cost=",cost[0]
