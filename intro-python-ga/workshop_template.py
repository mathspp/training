"""
This file uses the components in components.py to implement a simple genetic algorithm
to evolve a simple robot that cleans a room.
"""

from random import choice, shuffle, randint, random
from components import Directions, generate_room, render_whole_simulation, score_robot

GENERATIONS = 100
POPULATION_SIZE = 200
ROOMS = 10

ROOM_WIDTH = 15
ROOM_HEIGHT = 10
ROBOT_LENGTH = ROOM_WIDTH*ROOM_HEIGHT

def generate_robot(length):
    """Generate a random robot with the given length."""
    pass

def tournament_selection(scored_pop, rounds, bucket_size, pick_n):
    """Performs tournament selection.
    
    Performs the given amount of tournament selection rounds, where
    each round corresponds to creating buckets with the given size and
    picking the top `pick_n` elements.
    """
    pass

def crossover_reproduction(parents):
    """For every consecutive pair of robots, create two offspring."""
    pass

def mutate(offspring, rate):
    """Mutate each gene with probability given by the rate."""
    pass

if __name__ == "__main__":
    
    pop = None
    rooms = None
    max_scores = None
    top_robots = None

    # EA loop

    # Render the results
    #render_whole_simulation(top_robots, rooms)