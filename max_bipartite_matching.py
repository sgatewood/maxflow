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

def get_limits(info_filename):
    out = {}
    if info_filename == None:
        return {}
    for lst in maxflow.get_data(info_filename):
        out[lst[0]] = int(lst[1])
    return out

def get_graph(filename,chooser_info_filename=None,prize_info_filename=None):
    """
    chooser_info_filename: csv file that says how many prizes each person can win
    prize_info_filename: csv that that says how many people can win each prize
    Both are defaulted to 1
    """

    graph = maxflow.get_graph(filename)

    sources = set()
    destinations = set()

    chooser_limits = get_limits(chooser_info_filename)
    prize_limits = get_limits(prize_info_filename)

    for lst in graph.values():
        for edge in lst:
            sources.add(edge.src)
            destinations.add(edge.dest)

    check_source_and_sink_names(sources.union(destinations))
    check_choices_and_choosers_are_different(sources,destinations)

    graph[SOURCE] = [maxflow.Edge(SOURCE,dest,chooser_limits.get(dest,1)) for dest in sources]
    for src in destinations:
        graph.setdefault(src,[]).append(maxflow.Edge(src,SINK,prize_limits.get(src,1)))

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

if __name__ == "__main__":
    graph = get_graph("choices.csv",prize_info_filename="prize_info.csv")
    # maxflow.print_graph(graph)
    # print("-"*20)

    prizes = get_max_bipartite_matching(graph)
    print(prizes)
