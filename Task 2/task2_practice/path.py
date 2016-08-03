graph = {1: set([3, 2]),
         2: set([4, 1, 5]),
         3: set([5, 6]),
         4: set([5]),
         5: set([6, 7]),
         6: set([5, 7])}
print graph
def bfs(graph, start):
    visited, queue = set(), [start]
    
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
            print visited
    
    return visited



def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
                
            else:
                queue.append((next, path + [next]))

#list(bfs_paths(graph, 'A', 'F')) # [['A', 'C', 'F'], ['A', 'B', 'E', 'F']]

def shortest_path(graph, start, goal):
    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None

#shortest_path(graph, 'A', 'F') # ['A', 'C', 'F']
print "Shortest path", shortest_path(graph, 1, 7)
print list(bfs_paths(graph, 1, 7))
