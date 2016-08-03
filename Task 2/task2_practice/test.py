G={}
i=1
j=0
coordX={}
coordy={}
obs=[0]
routelength=0


'''for x in range(len(obs)):
    X=obs()
    
print 'coordX =',coordX,'coordY=',coordY'''
def neighbors(node):
    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    result = []
    for dir in dirs:
        neighbor = (node[0]-1 + dir[0])*10+(node[1] + dir[1])
        
        if 10*j+1 < neighbor<= 10*(j+1) :
            result.append(neighbor) 
            G.update({i: set(result)})
           
    #print result
   
'''for i in range(0,10):
    #G.update({i: [i+1,i+10,i-1,i-10]})''' 

all_nodes = []
for x in range(1,11):
    for y in range(1,11):
        all_nodes.append([x,y])
        
        neighbors([x,y])
        i+=1


       

print G


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

Route= shortest_path(G, 1, 10)
print Route
routelength=len(Route)
print routelength


#print list(bfs_paths(G, 5, 10))
