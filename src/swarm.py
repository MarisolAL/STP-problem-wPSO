import copy
import src.particle as particle


class Swarm:
    """
    Class that models a particle swarm

    Attributes
    ----------
    population: list
        List of particles in the swarm
    best_global: tuple
        Particle with the best fitness value in the swarm during all iterations
    fitness: function
        Function that evaluates the fitness of a particle
    """

    def __init__(self, population_size, initial_position, fitness_function):
        """
        Swarm class constructor
        Parameters
        ----------
        population_size: Int
            Number of particles in the swarm
        initial_position: list
            Initial position where the particles will be initialized
        fitness_function: function
            Function that evaluates the fitness of a particle
        """
        self.population = []
        self.best_global = None
        for i in range(population_size):
            particle_i = particle.Particle(initial_position, fitness_function)
            if i == 0:
                self.best_global = copy.copy(particle_i)
            if self.best_global.fitness > particle_i.fitness:
                self.best_global = copy.copy(particle_i)
            self.population.append(particle_i)
        self.fitness = fitness_function

    def particle_swarm_optimization(self, lower_limit, upper_limit, max_iterations):
        """
        Function that models the particle swarm optimization algorithm
        Parameters
        ----------
        lower_limit: list
            Lower limit of the search space
        upper_limit: list
            Upper limit of the search space
        max_iterations: Int
            Maximum number of iterations the algorithm will do
        Returns
        -------
        particle.Particle
            Particle with the best fitness value
        """
        iteration = 0
        iteration_without_improvement = 0
        while iteration < max_iterations and iteration_without_improvement <= 35:
            previous_global_best = copy.copy(self.best_global)
            for k in range(len(self.population)):
                particle_k = self.population[k]
                if particle_k.fitness < self.best_global.fitness:
                    self.best_global = copy.copy(particle_k)
                    iteration_without_improvement = 0

            for k in range(len(self.population)):
                particle_k = self.population[k]
                particle_k.update_state(lower_limit, upper_limit, self.best_global.position)
            if previous_global_best.position == self.best_global.position:
                iteration_without_improvement += 1
            iteration += 1
        return self.best_global
