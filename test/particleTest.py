import src.particle as particle
import unittest


class ParticleTest(unittest.TestCase):
    def test_particle_constructor(self):
        p = particle.Particle([1, 1], sum)
        for v in p.speed:
            self.assertLessEqual(v, 1, 'The speed in each position should be between 0 and 1')
            self.assertGreaterEqual(v, 0, 'The speed in each position should be between 0 and 1')
        self.assertEqual(p.position, p.best_fitness[1], 'In the first iteration, the position is the same as in '
                                                        'best_fitness')
        self.assertEqual(p.worsening, 0, 'In the first iteration the particle haven´t worsened its position')
        self.assertLessEqual(p.best_fitness[0], 4, 'The first fitness is at best equal to 4')


if __name__ == '__main__':
    unittest.main()
