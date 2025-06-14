# Steiner Tree Problem with Particle Swarm Optimization

This project tackles the Euclidean Steiner Tree Problem (ESTP) using Particle Swarm Optimization (PSO). The goal is to approximate near-optimal solutions
for connecting a given set of terminal points in the plane with the minimal total length, possibly introducing additional Steiner points to reduce the total cost.

The algorithm simulates a swarm of particles exploring the solution space, leveraging PSO dynamics (position, velocity, personal/global bests) to find high-quality Steiner trees in a Euclidean setting.

## Problem Overview
### Euclidean Steiner Tree Problem (ESTP)

Given a set of points (terminals) in 2D space, the ESTP seeks the shortest interconnection of these points, allowing the addition of auxiliary points (Steiner points).
Finding the exact solution is NP-hard, making heuristic and metaheuristic approaches like PSO attractive for larger instances.

### Particle Swarm Optimization (PSO)

PSO is a population-based optimization algorithm inspired by the social behavior of birds and fish. Each particle represents a candidate Steiner tree configuration and
iteratively updates its position in the solution space based on:

* Its own best-known position (personal best)

* The global best position found by any particle

* Velocity updates guided by random and weighted components


## Technologies Used

This project is implemented in Python 3 and uses the following libraries:

* [NetworkX](https://networkx.org/documentation/stable/index.html)
* [Random](https://docs.python.org/3/library/random.html)
* [Numpy](https://numpy.org)
* [unittest](https://docs.python.org/3/library/unittest.html)
* [math](https://docs.python.org/3/library/math.html)
* [matplotlib](https://matplotlib.org)
* [json](https://docs.python.org/3/library/json.html)
* [copy](https://docs.python.org/3/library/copy.html)
