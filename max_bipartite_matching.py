import maxflow
# from maxflow import ford_fulkerson, get_graph, Edge

SOURCE = "SOURCE"
SINK = "SINK"

def check_source_and_sink_names(nodes):
    if SOURCE in nodes or SINK in nodes:
        raise Exception("Change SOURCE and SINK names")

def check_choices_and_choosers_are_different(sources,destinations):
    for source in sources:
        if source in destinations:
            raise Exception("Choices cannot have chooser names")

def get_graph(filename):

    graph = maxflow.get_graph(filename)

    sources = set()
    destinations = set()

    for lst in graph.values():
        for edge in lst:
            sources.add(edge.src)
            destinations.add(edge.dest)

    check_source_and_sink_names(sources.union(destinations))
    check_choices_and_choosers_are_different(sources,destinations)

    graph[SOURCE] = [maxflow.Edge(SOURCE,dest,1) for dest in sources]
    for src in destinations:
        graph.setdefault(src,[]).append(maxflow.Edge(src,SINK,1))

    return graph

def get_max_bipartite_matching(graph):
    flow = maxflow.ford_fulkerson(graph,source=SOURCE,sink=SINK)
    # print(flow)
    # options = graph[SINK]
    winners = [edge for edge in graph[SOURCE] if edge.value > 0]
    prizes = {}
    for edge in winners:
        winner = edge.dest
        prizes[winner] = [e.dest for e in graph[winner] if e.value > 0 and e.dest != SOURCE]

    return prizes

graph = get_graph("choices.csv")
# maxflow.print_graph(graph)
# print("-"*20)

prizes = get_max_bipartite_matching(graph)
print(prizes)
