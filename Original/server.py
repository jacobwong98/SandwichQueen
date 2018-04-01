from graph import Graph
from binary_heap import BinaryHeap
import math
from serial import Serial
from time import sleep


def checkinput():
    '''
        Check if the user has sent an A and will then print out the next waypoint
        Prevents missing a waypoint because if they don't input A, the method
        will recursively call and will get the user's input again
    '''

    ack = input().strip()
    if ack == 'A':
        print('W', latitude, longitude)
    else:
        checkinput()


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


def load_edmonton_graph(filename):
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
                latitude = int(float(lines[2]) * 100000)
                longitude = int(float(lines[3]) * 100000)
                location[int(lines[1])] = (latitude, longitude)

            elif lines[0] == "E":
                graph.add_edge((int(lines[1]), int(lines[2])))

    return graph, location


if __name__ == "__main__":
    yegGraph, location = load_edmonton_graph('edmonton-roads-2.0.1.txt')
    cost = CostDistance(location)
    with Serial("/dev/ttyACM0", baudrate=9600, timeout=1) as ser:

        while True:
            line = ser.readline()
            decodedLine = line.decode("ASCII")
            # Split the user input into a list
            selectPoints = decodedLine.rstrip('\n\r').split(" ")
            if not selectPoints:
                continue
            elif selectPoints[0] is 'R':
                # Change start and end entries into integers
                startcoord = [int(selectPoints[1]), int(selectPoints[2])]
                endcoord = [int(selectPoints[3]), int(selectPoints[4])]
                start = None
                end = None

                start, end = findmin(startcoord, endcoord, location)
                reached = least_cost_path(yegGraph, start, end, cost)

                if len(reached) > 0:
                    wayNum = "N " + str(len(reached)) + "\n"
                    print(wayNum)
                    encodedSend = wayNum.encode("ASCII")
                    ser.write(encodedSend)
                    continue

                else:
                    wayNum = "N 0\n"
                    encodedSend = wayNum.encode("ASCII")
                    ser.write(encodedSend)

            elif selectPoints[0] is 'A':
                    if len(reached) > 0:
                        point = location[reached.pop(0)]

                        lat = point[0]
                        lon = point[1]
                        message = "W " + str(lat) + " " + str(lon) + "\n"

                    else:
                        message = "E\n"

                    encodedSend = message.encode("ASCII")
                    ser.write(encodedSend)
                    continue
            else:
                align = "%"
                encodedSend = align.encode("ASCII")
                ser.write(encodedSend)

            sleep(2) # Sleepy Time
