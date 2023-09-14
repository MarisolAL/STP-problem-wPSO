import numpy as np
import random


class Particle:
    """
    Class that models a particle in a swarm

    Attributes
    ----------
    position : list
        Position where the particle is located
    speed: list
        List with the speed of the particle, one element per dimension
    worsening: int
        Times that a particle worsens their fitness
    fitness_function: function
        Function that evaluates the fitness of a particle
    fitness: float
        Fitness value of a particle
    best_fitness: tuple
        Tuple with position and fitness evaluation where the best fitness was found
    """

    def __init__(self, initial_position, fitness_function):
        """
        Parameters
        ----------
        initial_position: list
            Seed of the particle, from this position the particle will start to move
        fitness_function: function
            Function that will calculate the fitness of a particle
        """
        dimension = len(initial_position)
        self.position = []
        self.speed = []
        self.worsening = 0
        self.fitness_function = fitness_function
        for i in range(dimension):
            self.speed.append(random.uniform(0, 1))
            self.position.append(initial_position[i] + random.uniform(-1, 1))
        self.fitness = fitness_function(self.position)
        self.best_fitness = (self.fitness, self.position)

    def update_position(self, upper_limit, lower_limit):
        """
        Function that updates the position of a particle using the speed vector, if the new position exceeds the
        limits then the position will be equal to the limit it exceeds.
        Parameters
        ----------
        upper_limit: list
            Upper limit of the search space
        lower_limit: list
            Lower limit of the search space
        """
        new_position = []
        for i in range(len(self.position)):
            new_position.append(self.position[i] + self.speed[i])
            if new_position[i] > upper_limit[i]:
                new_position[i] = upper_limit[i]
            if new_position[i] < lower_limit[i]:
                new_position[i] = lower_limit[i]
        self.position = new_position

    def update_speed(self, best_global_position):
        """
        Function that updates the speed vector of a particle
        Parameters
        ----------
        best_global_position: list
            Position vector of the particle with the best fitness in the swarm
        """
        w = 0.5  # Inertia constant
        c_1 = 1.25  # Cognitive constant
        c_2 = 1.75  # Social constant

        r_1 = np.random.normal(0, 1, len(self.position))
        r_2 = np.random.normal(0, 1, len(self.position))

        cognitive_speed = []
        social_speed = []

        for i in range(len(self.position)):
            cognitive_speed.append(self.best_fitness[1][i] - self.position[i])
            social_speed.append(best_global_position[i] - self.position[i])

        new_speed = []
        for i in range(len(self.position)):
            momentum = w * self.speed[i]
            cognitive_section = c_1 * cognitive_speed[i] * r_1[i]
            social_section = c_2 * r_2[i] * social_speed[i]
            new_speed_value = momentum + social_section + cognitive_section
            new_speed.append(new_speed_value)
        self.speed = new_speed

    def update_fitness(self):
        """
        Function that updates the fitness value of a particle, checks if the new value is better than `best_fitness`
        or if the particle worsened the fitness value.
        """
        actual_position_fitness = self.fitness_function(self.position)
        self.fitness = actual_position_fitness
        if actual_position_fitness > self.best_fitness[0]:
            self.worsening += 1
        else:
            self.worsening = 0
            if actual_position_fitness < self.best_fitness[0]:
                self.best_fitness = (actual_position_fitness, self.position)

    def check_reset(self):
        """
        Function that checks if due to the worsening fitness times, the particle should be reset
        """
        if self.worsening >= 20:
            new_particle = Particle(self.position, self.fitness_function)
            self.position = new_particle.position
            self.speed = new_particle.speed
            self.worsening = 0
            self.fitness = new_particle.fitness
            self.best_fitness = new_particle.best_fitness

    def update_state(self, lower_limit, upper_limit, best_global_position):
        """
        Function that do an iteration of the living cycle of a particle by updating its parameters
        Parameters
        ----------
        lower_limit: list
            Lower limit of the search space
        upper_limit: list
            Upper limit of the search space
        best_global_position: list
            Position vector of the particle with the best fitness in the swarm
        """
        self.check_reset()
        self.update_fitness()
        self.update_speed(best_global_position)
        self.update_position(upper_limit, lower_limit)
