"""
This file uses the components in components.py to implement a simple genetic algorithm
to evolve a simple robot that cleans a room.
"""

from random import choice, shuffle, randint, random
from components import Directions, generate_room, render_whole_simulation, score_robot, create_frame_dump

GENERATIONS = 100
POPULATION_SIZE = 300
ROOMS = 10

ROOM_WIDTH = 8
ROOM_HEIGHT = 6
ROBOT_LENGTH = ROOM_WIDTH*ROOM_HEIGHT

def generate_robot(length):
    """Generate a random robot with the given length."""

    dirs = [Directions.LEFT, Directions.RIGHT, Directions.UP, Directions.DOWN]
    robot = [choice(dirs) for _ in range(length)]
    return robot

def tournament_selection(scored_pop, rounds, bucket_size, pick_n):
    """Performs tournament selection.
    
    Performs the given amount of tournament selection rounds, where
    each round corresponds to creating buckets with the given size and
    picking the top `pick_n` elements.
    """
    chosen = []

    for _ in range(rounds):
        shuffle(scored_pop)

        # Go over each bucket
        for i in range(len(scored_pop)//bucket_size):
            # Sort the bucket
            bucket = scored_pop[i*bucket_size:(i+1)*bucket_size]
            sorted_bucket = sorted(bucket, reverse = True)
            # and pick the top members
            for n in range(pick_n):
                chosen.append(
                    [value for value in sorted_bucket[n][1]]
                )
    
    return chosen

def crossover_reproduction(parents):
    """For every consecutive pair of robots, create two offspring."""

    offspring = []
    for pair_idx in range(len(parents)//2):
        father = parents[pair_idx*2]
        mother = parents[pair_idx*2 + 1]

        cutoff = randint(0, len(father))

        son = father[:cutoff] + mother[cutoff:]
        daughter = mother[:cutoff] + father[cutoff:]
        offspring.append(son)
        offspring.append(daughter)

    return offspring

def mutate(offspring, rate):
    """Mutate each gene with probability given by the rate."""
    
    dirs = [Directions.LEFT, Directions.RIGHT, Directions.UP, Directions.DOWN]

    for child in offspring:
        for i in range(len(child)):
            if random() < rate:
                child[i] = choice(dirs)

if __name__ == "__main__":
    
    pop = [generate_robot(ROBOT_LENGTH) for _ in range(POPULATION_SIZE)]
    rooms = [generate_room(ROOM_WIDTH, ROOM_HEIGHT) for _ in range(ROOMS)]
    max_scores = []
    for room in rooms:
        acc = 0
        for row in room:
            acc += sum(row)
        max_scores.append(acc)
    max_score = sum(max_scores)

    top_robots = []

    for gen in range(GENERATIONS):

        scores = [[score_robot(robot, room) for room in rooms] for robot in pop]
        scores = map(sum, scores)
        
        scored_robots = sorted(zip(scores, pop), reverse = True)

        print("Generation {:3} - {}".format(gen, round(100*scored_robots[0][0]/max_score, 2)))
        
        top_robot = scored_robots[0][1][::]
        top_robots.append(top_robot)

        chosen = tournament_selection(scored_robots, 2, 4, 2)
        offspring = crossover_reproduction(chosen)
        mutate(offspring, 0.005)

        pop = offspring[::]

        while len(pop) < POPULATION_SIZE:
            chosen.append(generate_robot(ROBOT_LENGTH))

    #render_whole_simulation(top_robots, rooms)

    create_frame_dump("worst_imgbin", top_robots[0], rooms[0])
    create_frame_dump("top_imgbin", top_robots[-1], rooms[0])