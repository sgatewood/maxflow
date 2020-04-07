
def get_data(filename):
    with open(filename) as y:
        for line in y:
            yield line.strip().split(",")

def red(s):
    return "\033[1;31m%s\033[0m" % s

# def cyan(s):
#     return "\033[1;36m%s\033[0m" % s

class Edge:

    def __init__(self,src,dest,capacity,value=0,aug=None):
        self.src = src
        self.dest = dest
        self.capacity = capacity
        self.value = value
        self.aug = aug

    def __str__(self):
        return "%s -> %s (%d/%d)" % (red(self.src),self.dest,self.value,self.capacity)

    def get_potential(self):
        return self.capacity - self.value

    @classmethod
    def link(cls,edge1,edge2):
        edge1.aug = edge2
        edge2.aug = edge1

    def _check_capacity(self):
        if self.value > self.capacity or self.value < 0:
            raise Exception("Bad edge: " + str(self))

    def addFlow(self,flow):
        self.value += flow
        self.aug.value -= flow
        self._check_capacity()
        self.aug._check_capacity()

# def print_graph(graph):
#     for key in graph:
#         # print(key)
#         for edge in graph[key]:
#             print(edge)

def get_graph(filename):
    graph = {}
    for lst in get_data(filename):
        src,dest = lst[:2]
        capacity = 0
        if len(lst) >= 3:
            capacity = int(lst[2])

        if src not in graph:
            graph[src] = []

        if dest not in graph:
            graph[dest] = []

        edge = Edge(src,dest,capacity)
        aug = Edge(dest,src,capacity,capacity)
        Edge.link(edge,aug)

        graph[src].append(edge)
        graph[dest].append(aug)

    return graph

def get_aug_path(graph,src,sink):
    paths = []
    for edge in graph[src]:
        if edge.value >= edge.capacity:
            continue
        paths.append([edge])
    while len(paths) != 0:
        # print(len(paths),len(paths[0]),paths[0][-1].src)
        path = paths.pop(0)
        end = path[-1].dest
        if end == sink:
            return path
        found = True
        for edge in graph[end]:
            if edge.dest in map(lambda e: e.src,path) or edge.value >= edge.capacity:
                continue
            newPath = path + [edge]
            # if newPath[0] == None or edge.get_potential() < newPath[0]:
            #     newPath[0] = edge.get_potential()
            #     print(edge,newPath[0],sep="|||")
            paths.append(newPath)

def ford_fulkerson(graph,src="S",sink="T"):
    # print_graph(graph)

    path = get_aug_path(graph,src,sink)
    while path != None:
        flow = min(map(Edge.get_potential,path))
        print("|".join(map(str,path)),"(flow = %d)" % flow)

        for edge in path:
            edge.addFlow(flow)

        path = get_aug_path(graph,src,sink)
        # input()

graph = get_graph("graph.csv")
ford_fulkerson(graph)
