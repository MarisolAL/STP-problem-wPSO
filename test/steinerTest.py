import src.steiner as steiner
import unittest
from src.util import calculate_total_graph_weight


class SteinerTest(unittest.TestCase):
    def test_steiner_constructor(self):
        s = steiner.Steiner([(0, 0), (0, 1), (2, 0)])
        self.assertEqual(len(s.points), 3)
        self.assertEqual(s.tree, None)
        self.assertEqual(s.weight, None)

    def test_calculate_tree(self):
        s = steiner.Steiner([(0, 0), (0, 1), (2, 0)])
        s.calculate_minimum_euclidean_tree()
        self.assertEqual(len(s.tree.edges), 2)

    def test_total_weight(self):
        s = steiner.Steiner([(0, 0), (0, 1), (2, 0)])
        s.calculate_minimum_euclidean_tree()
        s.calculate_total_tree_weight()
        self.assertEqual(s.weight, 3)

    def test_calculate_tree_with_point(self):
        s = steiner.Steiner([(0, 0), (0, 1), (2, 0)])
        s.calculate_minimum_euclidean_tree()
        new_tree = s.calculate_tree_with_point((1, 1))
        self.assertEqual(len(new_tree.edges), 3, 'The total number of edges should be 3')
        new_tree_weight = calculate_total_graph_weight(new_tree)
        self.assertLessEqual(new_tree_weight, 3.5, 'The total weight of the new tree should be less than 3.5')

    def test_upper_limit(self):
        s = steiner.Steiner([(-9, 8), (-7, 3), (-2, 7), (9, 9),
                             (10, -8), (-10, 9), (4, 0)])
        upper_limit = s.calculate_upper_limit()
        self.assertEqual(upper_limit, [10, 9])

    def test_lower_limit(self):
        s = steiner.Steiner([(-9, 8), (-7, 3), (-2, 7), (9, 9),
                             (10, -8), (-10, 9), (4, 0)])
        lower_limit = s.calculate_lower_limit()
        self.assertEqual(lower_limit, [-10, -8])

    def test_steiner_optimization(self):
        s = steiner.Steiner([(-4, 0), (0, 6), (4, 0)])
        s.calculate_minimum_euclidean_tree()
        s.calculate_total_tree_weight()
        steiner_points = s.steiner_particle_optimization(30, 10, 15)
        self.assertGreaterEqual(len(steiner_points[0]), len(s.points))
        self.assertLessEqual(steiner_points[1], s.weight)


if __name__ == '__main__':
    unittest.main()
