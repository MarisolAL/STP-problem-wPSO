import src.swarm as swarm
import src.particle as particle
import unittest


class SwarmTest(unittest.TestCase):
    def test_swarm_constructor(self):
        s = swarm.Swarm(5, [0, 0], sum)
        self.assertEqual(len(s.population), 5, 'The total amount of particles should be equal to the parameter')
        for p in s.population:
            self.assertIsInstance(p, particle.Particle, 'Every item in the swarm should be a particle')
        self.assertEqual(s.fitness, sum, 'The fitness function should be equal to the parameter')


if __name__ == '__main__':
    unittest.main()
