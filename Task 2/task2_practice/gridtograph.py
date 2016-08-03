graph=[[] for i in range(100)]
grid_map= [ [ 0 for i in range(10) ] for j in range(10) ]
def neighbors(node):
    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    result = []
    for dir in dirs:
        neighbor = [node[0] + dir[0], node[1] + dir[1]]
        if 0 <= neighbor[0] < 10 and 0 <= neighbor[1] < 10:
            result.append(neighbor)
            graph[node].append(neighbor)
    print result
    


all_nodes = []
for x in range(10):
    for y in range(10):
        all_nodes.append([x,y])
        neighbors([x,y])

        

def bfs(graph, start):
    visited, queue = set(), [start]
    
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
            print visited
    
    return visited



