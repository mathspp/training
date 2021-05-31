from random import choice, random, randint, shuffle
from components import render_whole_simulation

ROOM_WIDTH = 14
ROOM_HEIGHT = 8
ROOMS = 10
ROBOTS = 300
ROBOT_LENGTH = ROOM_WIDTH * ROOM_HEIGHT

GENERATIONS = 100

class Directions:
    LEFT = [-1, 0]
    RIGHT = [1, 0]
    UP = [0, -1]
    DOWN = [0, 1]
    STILL = [0, 0]

    ALL = [LEFT, RIGHT, UP, DOWN, STILL]

def generate_robot(length):
    return [choice(Directions.ALL) for _ in range(length)]

def generate_room(width, height):
    return [
        [random() for _ in range(width)] for _ in range(height)
    ]

def score_robot(robot, room):
    room_ = [row[:] for row in room]
    posx, posy = ROOM_WIDTH//2, ROOM_HEIGHT//2
    score = room_[posy][posx]
    room_[posy][posx] = 0

    while robot:
        step, *robot = robot
        posx = min(max(posx + step[0], 0), ROOM_WIDTH - 1)
        posy = min(max(posy + step[1], 0), ROOM_HEIGHT - 1)
        score += room_[posy][posx]
        room_[posy][posx] = 0

    return score

def crossover_reproduction(r1, r2):
    crossover = randint(1, len(r1) - 1)
    s1 = r1[:crossover] + r2[crossover:]
    s2 = r2[:crossover] + r1[crossover:]
    return s1, s2

def mutation(robot):
    prob = 0.001
    for i in range(len(robot)):
        if random() < prob:
            robot[i] = choice(Directions.ALL)
    return robot


if __name__ == "__main__":
    # Create random initial population.
    population = [generate_robot(ROBOT_LENGTH) for _ in range(ROBOTS)]
    rooms = [generate_room(ROOM_WIDTH, ROOM_HEIGHT) for _ in range(ROOMS)]
    best_robots = []

    # As generations pass:
    for gen in range(GENERATIONS):
        # Assess each robot.
        scores = [
            sum(score_robot(robot, room) for room in rooms)
            for robot in population
        ]

        scored_robots = sorted(zip(scores, population))
        # Truncation selection.
        population = [
            robot for _, robot in scored_robots[ROBOTS//2:]
        ]
        best = scored_robots[-1]
        best_robots.append(best[1])
        ## f-strings / format strings for string interpolation.
        print(f"{gen} : {best[0]}, {best[1].count(Directions.STILL)}")

        shuffle(population)
        offspring = []
        for p1, p2 in zip(population[::2], population[1::2]):
            offspring.extend(crossover_reproduction(p1, p2))

        population += offspring
        population = [mutation(robot) for robot in population]

    render_whole_simulation(best_robots, rooms)
