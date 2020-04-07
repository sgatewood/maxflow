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
        self._check_capacity()

        self.aug.value -= flow
        self.aug._check_capacity()

def print_graph(graph):
    for key in graph:
        # print(key)
        for edge in graph[key]:
            print(edge)

def get_data(filename):
    with open(filename) as y:
        for line in y:
            yield line.strip().split(",")

def get_graph(filename):
    graph = {}
    for lst in get_data(filename):
        src = lst[0]
        dest = lst[1]
        capacity = 1 if len(lst) < 3 else int(lst[2])

        edge = Edge(src,dest,capacity)

        graph.setdefault(src,[]).append(edge)

    return graph

def add_aug_paths(graph):
    edges = []
    for lst in graph.values():
        edges.extend(lst)

    for edge in edges:
        src,dest,capacity = edge.src,edge.dest,edge.capacity
        aug = Edge(dest,src,capacity,capacity)
        Edge.link(edge,aug)

        graph.setdefault(dest,[]).append(aug)

def print_path(path):
    for edge in path:
        print(edge,end=",")
    print()

def get_aug_path(graph,src,sink):
    paths = [[edge] for edge in graph[src] if edge.value < edge.capacity]

    while len(paths) > 0:
        path = paths.pop(0)
        end = path[-1].dest

        if end == sink:
            return path

        for edge in graph[end]:
            if edge.dest in map(lambda e: e.src,path) or edge.value >= edge.capacity:
                continue
            paths.append(path + [edge])

def ford_fulkerson(graph,source="S",sink="T"):
    """Mutates graph and returns total flow"""

    add_aug_paths(graph)

    # print_graph(graph)

    total_flow = 0

    path = get_aug_path(graph,source,sink)
    while path != None:
        flow = min(map(Edge.get_potential,path))
        # print("|".join(map(str,path)),"(flow = %d)" % flow)

        for edge in path:
            edge.addFlow(flow)

        path = get_aug_path(graph,source,sink)
        total_flow += flow
        # input()

    return total_flow

if __name__ == "__main__":
    graph = get_graph("graph.csv")
    print(ford_fulkerson(graph))
