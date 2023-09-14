import math
import networkx as nx
import src.swarm as swarm
from src.util import distance_between_two_points, calculate_total_graph_weight
import random


class Steiner:
    """
    Class that models the Euclidean Steiner Tree Problem

    Attributes
    ----------
    points: list
        Points that belong to the initial set of the problem instance
    tree: nx. Graph
        List of edges that belong to the original euclidean minimum spanning tree
    weight: float
        Weight of the tree
    """

    def __init__(self, points):
        """
        Steiner class constructor
        Parameters
        ----------
        points: list
            Points that belong to the initial set of the problem instance
        """
        self.points = points
        self.tree = None
        self.weight = None

    def set_steiner(self, points):
        """
        Steiner class setter
        Parameters
        ----------
        points: list
            Points that will be set to the tree
        """
        self.points = points
        self.tree = None
        self.weight = None

    def delete_steiner(self):
        """
        Function that deletes the object data
        """
        self.points = []
        self.weight = 0
        self.tree = None

    def calculate_minimum_euclidean_tree(self):
        """
        Function that calculates the euclidean minimum spanning tree of the points set.
        """
        graph = nx.Graph()
        for point_i in self.points:
            graph.add_node(tuple(point_i))
        for point_i in self.points:
            for point_j in self.points:
                if (not point_i == point_j) \
                        and (not graph.has_edge(tuple(point_i), tuple(point_j))):
                    weight = distance_between_two_points(point_i, point_j)
                    graph.add_edge(tuple(point_i), tuple(point_j), weight=weight)
        tree = nx.minimum_spanning_tree(graph)
        for edge_i in tree.edges:
            weight = distance_between_two_points(edge_i[0], edge_i[1])
            tree.add_edge(edge_i[0], edge_i[1], weight=weight)
        self.tree = tree

    def calculate_total_tree_weight(self):
        """
        Function that calculates the total weight of the tree and sets it to `weight` attribute.
        """
        self.weight = calculate_total_graph_weight(self.tree)

    def calculate_tree_with_point(self, point):
        """
        Function that given a point, calculates the euclidean minimum spanning tree of the initial point
        set and the given point
        Parameters
        ----------
        point: tuple
            Point added to the initial points set to calculate the tree.
        Returns
        -------
        nx.Graph
            Euclidean minimum spanning tree that includes the new point in the vertex set
        """
        new_points = self.points + [point]
        new_steiner = Steiner(new_points)
        new_steiner.calculate_minimum_euclidean_tree()
        return new_steiner.tree

    def calculate_upper_limit(self):
        """
        Function that calculates the upper limit (maximum coordinates) of the points set
        Returns
        -------
        list
            List with the value of the maximum coordinates
        """
        x_max = self.points[0][0]
        y_max = self.points[0][1]
        for point in self.points:
            if point[0] > x_max:
                x_max = point[0]
            if point[1] > y_max:
                y_max = point[1]
        return [x_max, y_max]

    def calculate_lower_limit(self):
        """
        Function that calculates the upper limit (minimum coordinates) of the points set
        Returns
        -------
        list
            List with the value of the minimum coordinates
        """
        x_min = self.points[0][0]
        y_min = self.points[0][1]
        for point in self.points:
            if point[0] < x_min:
                x_min = point[0]
            if point[1] < y_min:
                y_min = point[1]
        return [x_min, y_min]

    def stp_fitness(self, new_point):
        """
        Function that calculates the Steiner Tree Problem (STP) fitness of a new point
        Parameters
        ----------
        new_point: tuple
            Point that will be added to the preexisting graph
        Returns
        -------
        float
            Weight of the new tree
        """
        new_tree = self.calculate_tree_with_point(new_point)
        new_tree_weight = calculate_total_graph_weight(new_tree)
        return new_tree_weight

    def steiner_particle_optimization(self, max_iterations, swarms_amount, population_size, max_points=math.inf):
        """
        Function that executes the Particle Swarm Optimization algorithm for the Steiner Tree Problem
        Parameters
        ----------
        max_iterations: int
            Maximum number of iterations for each swarm
        swarms_amount: int
            Swarm amount that will be initialized one by one
        population_size: int
            Population size for the swarms, every swarm will have the same size
        max_points: int
            Maximum number of points added to the original tree
        Returns
        -------
        list
            List with the original points, the final weight of the graph and the steiner points found
        """
        print("Original weight ", str(self.weight))
        up_lim = self.calculate_upper_limit()
        low_lim = self.calculate_lower_limit()
        new_steiner_points = []
        actual_swarm = 0
        while actual_swarm < swarms_amount and len(new_steiner_points) < max_points:
            x_initial = random.uniform(low_lim[0], up_lim[0])
            y_initial = random.uniform(low_lim[1], up_lim[1])
            initial_position = [x_initial, y_initial]
            swarm_i = swarm.Swarm(population_size, initial_position, self.stp_fitness)
            best_particle = swarm_i.particle_swarm_optimization(low_lim, up_lim, max_iterations)
            new_steiner_p = best_particle.position
            new_steiner_fitness = best_particle.fitness
            if new_steiner_fitness < self.weight:
                new_steiner_points.append(new_steiner_p)
                self.points.append(new_steiner_p)
                self.calculate_minimum_euclidean_tree()
                self.calculate_total_tree_weight()
            actual_swarm += 1
        print("Final weight ", self.weight, " with the points ", self.points)
        return [self.points, self.weight, new_steiner_points]
