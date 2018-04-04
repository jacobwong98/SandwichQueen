'''
Contains the stuff that will calculate the least_cost_path
'''
from binaryHeap import BinaryHeap
from graph import Graph
import math

def findmin(s, end, loc):
    '''
    This function will find the closest vertex from the user's coordinates
    s - list of the user's starting latitude/longitude
    end- list of the user's final latitude/longitude
    loc- dictionary that has the vertex identifier as key and a tuple of the
        latitude/longitude from the edmonton graph text file

    Returns:
    minStartVert - find the ID of the closest vertex from the starting point
    minEndVert - find the ID of the closest vertex from the final point
    '''
    minStart = float("inf")
    minEnd = float("inf")
    minStartVert = None
    minEndVert = None

    for vert, tup in loc.items():
        # use Manhatten distance to find the smallest distance to start point
        if (abs(tup[0] - s[0]) + abs(tup[1] - s[1])) <= minStart:
            minStartVert = vert
            minStart = abs(tup[0] - s[0]) + abs(tup[1] - s[1])
        # use Manhatten distance to find the smallest distance to end point
        if (abs(tup[0] - end[0]) + abs(tup[1] - end[1])) <= minEnd:
            minEndVert = vert
            minEnd = abs(tup[0] - end[0]) + abs(tup[1] - end[1])

    return minStartVert, minEndVert

def least_cost_path(graph, start, dest, cost):
    """Find and return a least cost path in graph from start
    vertex to dest vertex.
    Efficiency: If E is the number of edges, the run-time is
    O( E log(E) ).
    Args:
    graph (Graph): The digraph defining the edges between the
    vertices.
    start: The vertex where the path starts. It is assumed
    that start is a vertex of graph.
    dest:  The vertex where the path ends. It is assumed
    that dest is a vertex of graph.
    cost:  A class with a method called "distance" that takes
    as input an edge (a pair of vertices) and returns the cost
    of the edge. For more details, see the CostDistance class
    description below.
    Returns:
    list: A potentially empty list (if no path can be found) of
    the vertices in the graph. If there was a path, the first
    vertex is always start, the last is always dest in the list.
    Any two consecutive vertices correspond to some
    edge in graph.
    """
    reached = {}  # empty dictionary
    events = BinaryHeap()  # empty heap
    events.insert((start, start), 0)  # vertex s burns at time 0

    while len(events) > 0:
        edge, time = events.popmin()
        if edge[1] not in reached:
            reached[edge[1]] = edge[0]
            for nbr in graph.neighbours(edge[1]):
                events.insert((edge[1], nbr), time + cost.distance((edge[1], nbr)))
    # if the dest is not in reached, then no route was found
    if dest not in reached:
        return []

    current = dest
    route = [current]
    # go through the reached vertices until we get back to start and append
    # each vertice that we "stop" at
    while current != start:
        current = reached[current]
        route.append(current)
    # reverse the list because we made a list that went from the dest to start
    route = route[::-1]
    return route


class CostDistance():
    """
    A class with a method called distance that will return the Euclidean
    between two given vertices.
    """
    def __init__(self, location):
        """
        Creates an instance of the CostDistance class and stores the
        dictionary "location" as a member of this class.
        """
        self.locDict = location

    def distance(self, e):
        """
        Here e is a pair (u,v) of vertices.
        Returns the Euclidean distance between the two vertices u and v.
        """
        lon1, lat1 = self.locDict[e[0]]
        lon2, lat2 = self.locDict[e[1]]
        edist = math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)
        return edist


def load_graph(filename):
    """
    Loads the graph of Edmonton from the given file.
    Returns two items
    graph: the instance of the class Graph() corresponding to the
    directed graph from edmonton-roads-2.0.1.txt
    location: a dictionary mapping the identifier of a vertex to
    the pair (lat, lon) of geographic coordinates for that vertex.
    These should be integers measuring the lat/lon in 100000-ths
    of a degree.
    In particular, the return statement in your code should be
    return graph, location
    (or whatever name you use for the variables).
    Note: the vertex identifiers should be converted to integers
    before being added to the graph and the dictionary.
    """
    with open(filename, 'r') as filename:
        graph = Graph()
        location = {}

        for line in filename:
            lines = line.strip().split(",")

            if lines[0] == "V":
                graph.add_vertex(int(lines[1]))
                x = int(lines[2])
                y = int(lines[3])
                location[int(lines[1])] = (x, y)

            elif lines[0] == "E":
                graph.add_edge((int(lines[1]), int(lines[2])))
                # graph.add_edge((int(lines[2]), int(lines[1])))

    return graph, location
