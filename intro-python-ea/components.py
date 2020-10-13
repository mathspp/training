import os.path

import pygame
import pygame.locals

pygame.display.init()

from random import random

class Directions(object):
    """Hold the directions in which the robot can walk."""

    LEFT = [-1, 0]
    RIGHT = [1, 0]
    UP = [0, -1]
    DOWN = [0, 1]
    STILL = [0, 0]

def generate_room(width, height):
    """Generate a 2D array of dimensions height x width with random values."""
    return [[random() for _ in range(width)] for _ in range(height)]

def score_robot(robot, room):
    """Given a room and a cleaning robot, score the cleaning of the robot.
    
    The robot is a list of Directions.
    The room is a 2D array with dimensions height x width.
    """
    
    score = 0
    width = len(room[0])
    height = len(room)
    posx, posy = width//2, height//2

    # Create a deep copy of the room in case we need the original room
    room_copy = [[val for val in row] for row in room]

    for dx, dy in robot:
        score += room_copy[posy][posx]
        room_copy[posy][posx] = 0
        posx = max(min(posx + dx, width - 1), 0)
        posy = max(min(posy + dy, height - 1), 0)
    score += room_copy[posy][posx]
    room_copy[posy][posx] = 0

    return score

# pygame-related global variables
FPS = 60
SQUARESIZE = 40
VELOCITY = 8
WAITING = 3
ROBOT_COLOUR = (230, 230, 0)
WHITE = (255, 255, 255)

def draw_room(screen, room):
    """Takes a room and draws it."""
    rect = pygame.Rect(0, 0, SQUARESIZE, SQUARESIZE)

    for y, row in enumerate(room):
        for x, value in enumerate(row):
            rect.left = x * SQUARESIZE
            rect.top = y * SQUARESIZE
            # the level of dirtiness shows in different shades of gray
            gray = [int((1 - value) * 255)] * 3
            pygame.draw.rect(screen, gray, rect)

def init_simulation(screen, room):
    """Helper method used by the rendering functions."""
    width = len(room[0])
    height = len(room)

    robot_left = (width // 2) * SQUARESIZE
    robot_top = (height // 2) * SQUARESIZE
    robot_rect = pygame.Rect(robot_left, robot_top, SQUARESIZE, SQUARESIZE)

    draw_room(screen, room)

    arrived = True # flags if the robot arrived at a square
    robot_idx = 0
    waiting = 0 # number of frames paused between directions
    direction = None # the direction we are moving in

    return robot_rect, arrived, robot_idx, waiting, direction

def create_frame_dump(folder, robot, room):
    """Given a room and a robot, save all the frames to create a movie."""
    
    width = len(room[0])
    height = len(room)

    WIDTH = SQUARESIZE * width
    HEIGHT = SQUARESIZE * height
    screen = pygame.Surface((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    robot_rect, arrived, robot_idx, _, direction = init_simulation(screen, room)

    going = True
    paused = False
    frame = 0
    while going:
        clock.tick(FPS)

        for ev in pygame.event.get():
            if ev.type == pygame.locals.QUIT:
                going = False

        # Only try moving the robot while there are movements to consider
        if robot_idx < len(robot) and not paused:
            if arrived:
                direction = robot[robot_idx]
                arrived = False

            else:
                pygame.draw.rect(screen, WHITE, robot_rect)

                robot_rect.left = max(robot_rect.left + VELOCITY*direction[0], 0)
                robot_rect.right = min(robot_rect.right, WIDTH)
                robot_rect.top = max(robot_rect.top + VELOCITY*direction[1], 0)
                robot_rect.bottom = min(robot_rect.bottom, HEIGHT)

                if (robot_rect.left % SQUARESIZE == 0) and (robot_rect.top % SQUARESIZE == 0):
                    arrived = True
                    robot_idx += 1
                    print("Move: {:3}".format(robot_idx))

                pygame.draw.rect(screen, ROBOT_COLOUR, robot_rect)
        else:
            going = False

        pygame.image.save(screen, os.path.join(folder, "frame{:06}.png".format(frame)))
        frame += 1

def render_whole_simulation(robots, rooms):
    """Use pygame to render the robot cleaning a given room."""

    robot_from_gen = 0
    room_idx = 0

    robot = robots[robot_from_gen]
    room = rooms[room_idx]

    width = len(room[0])
    height = len(room)

    WIDTH = SQUARESIZE * width
    HEIGHT = SQUARESIZE * height
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Robot from gen {}, room {}".format(robot_from_gen, room_idx))

    clock = pygame.time.Clock()

    robot_rect, arrived, robot_idx, waiting, direction = init_simulation(screen, room)

    going = True
    paused = False
    while going:
        clock.tick(FPS)

        for ev in pygame.event.get():
            if ev.type == pygame.locals.QUIT:
                going = False
            elif ev.type == pygame.locals.KEYDOWN:
                if ev.key == pygame.locals.K_p or ev.key == pygame.locals.K_SPACE:
                    paused = not paused

                elif ev.key == pygame.locals.K_UP:
                    robot_from_gen = (robot_from_gen - 1) % len(robots)
                    robot = robots[robot_from_gen]
                    robot_rect, arrived, robot_idx, waiting, direction = init_simulation(screen, room)
                    pygame.display.set_caption("Robot from gen {}, room {}".format(robot_from_gen, room_idx))
                elif ev.key == pygame.locals.K_DOWN:
                    robot_from_gen = (robot_from_gen + 1) % len(robots)
                    robot = robots[robot_from_gen]
                    robot_rect, arrived, robot_idx, waiting, direction = init_simulation(screen, room)
                    pygame.display.set_caption("Robot from gen {}, room {}".format(robot_from_gen, room_idx))
                elif ev.key == pygame.locals.K_LEFT:
                    room_idx = (room_idx - 1) % len(rooms)
                    room = rooms[room_idx]
                    robot_rect, arrived, robot_idx, waiting, direction = init_simulation(screen, room)
                    pygame.display.set_caption("Robot from gen {}, room {}".format(robot_from_gen, room_idx))
                elif ev.key == pygame.locals.K_RIGHT:
                    room_idx = (room_idx + 1) % len(rooms)
                    room = rooms[room_idx]
                    robot_rect, arrived, robot_idx, waiting, direction = init_simulation(screen, room)
                    pygame.display.set_caption("Robot from gen {}, room {}".format(robot_from_gen, room_idx))

        # Only try moving the robot while there are movements to consider
        if robot_idx < len(robot) and not paused:
            if waiting:
                waiting -= 1

            elif arrived:
                direction = robot[robot_idx]
                arrived = False

            else:
                pygame.draw.rect(screen, WHITE, robot_rect)

                robot_rect.left = max(robot_rect.left + VELOCITY*direction[0], 0)
                robot_rect.right = min(robot_rect.right, WIDTH)
                robot_rect.top = max(robot_rect.top + VELOCITY*direction[1], 0)
                robot_rect.bottom = min(robot_rect.bottom, HEIGHT)

                if (robot_rect.left % SQUARESIZE == 0) and (robot_rect.top % SQUARESIZE == 0):
                    arrived = True
                    waiting = WAITING
                    robot_idx += 1

                pygame.draw.rect(screen, ROBOT_COLOUR, robot_rect)

        pygame.display.flip()