import math
import networkx as nx


def distance_between_two_points(point_1, point_2):
    """Function that calculates the distance between two points with n-dimension."""
    distance = 0
    for i in range(0, len(point_1)):
        distance += pow((point_2[i] - point_1[i]), 2)
    return math.sqrt(distance)


def calculate_total_graph_weight(graph):
    """
    Function that calculates the total weight of a graph
    Parameters
    ----------
    graph: nx.Graph
        Graph which be used to calculate the weight using its edges
    Returns
    -------
    float
        Weight of the graph
    """
    total_weight = 0
    for edge in graph.edges.data('weight', default=1000):
        total_weight += edge[2]
    return total_weight
