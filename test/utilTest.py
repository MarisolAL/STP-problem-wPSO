import unittest
import networkx as nx
import src.util as util


class UtilTest(unittest.TestCase):
    def test_distance_between_two_points_base(self):
        point_1 = [0, 0]
        self.assertEqual(util.distance_between_two_points(point_1, point_1),
                         0,
                         "Should be 0")

    def test_distance_between_two_points(self):
        point_1 = [1, 1, 1]
        point_2 = [0, 1, 1]
        self.assertEqual(util.distance_between_two_points(point_1, point_2), 1, "Should be 1")

    def test_calculate_total_graph_weight(self):
        graph = nx.Graph()
        graph.add_node((0, 1))
        graph.add_node((0, 0))
        edge_weight = util.distance_between_two_points((0, 1), (0, 0))
        graph.add_edge((0, 1), (0, 0), weight=edge_weight)
        weight = util.calculate_total_graph_weight(graph)
        self.assertEqual(weight, 1, 'The weight should be equal to 1')


if __name__ == '__main__':
    unittest.main()
