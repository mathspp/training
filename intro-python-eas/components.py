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

def generate_room(width, height):
    """Generate a 2D array of dimensions height x width with random values."""
    return [[random() for _ in range(width)] for _ in range(height)]

def score_robot(robot, room):
    """Given a room and a cleaning robot, score the cleaning of the robot.
    
    The robot is a list of Directions.
    The room is a 2D array with dimensions height x width. The room is seen
        as a torus, meaning walking off the edge wraps around.
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
        posx = (posx + dx) % width
        posy = (posy + dy) % height
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

def draw_nice_rect(screen, width, height, colour, rect):
    """Draws a rectangle nicely in the screen with the given dimensions.

    If needed, wrap the drawing around the screen.
    """

    top_bot_parts = []

    # Check if we need to split the rectange horizontally
    if rect.bottom > height:
        top_bot_parts.append(
            pygame.Rect(rect.left, rect.top, rect.width, height - rect.top)
        )
        top_bot_parts.append(
            pygame.Rect(rect.left, 0, rect.width, rect.height + rect.top - height)
        )
    else:
        top_bot_parts.append(
            pygame.Rect(rect.left, rect.top, rect.width, rect.height)
        )

    parts = []
    for rect in top_bot_parts:
        if rect.right > width:
            parts.append(
                pygame.Rect(rect.left, rect.top, width - rect.left, rect.height)
            )
            parts.append(
                pygame.Rect(rect.left, rect.top, rect.width + rect.left - width, rect.height)
            )
        else:
            parts.append(
                rect
            )

    for rect in parts:
        pygame.draw.rect(screen, colour, rect)

def init_simulation(screen, room):
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

                if direction[0] == -1:
                    dir_name = "left"
                elif direction[0] == 1:
                    dir_name = "right"
                elif direction[1] == -1:
                    dir_name = "up"
                elif direction[1] == 1:
                    dir_name = "down"
                #pygame.display.set_caption("Movement {} going {}".format(robot_idx, dir_name))

            else:
                draw_nice_rect(screen, WIDTH, HEIGHT, WHITE, robot_rect)

                robot_rect.left = (robot_rect.left + VELOCITY*direction[0]) % WIDTH
                robot_rect.top = (robot_rect.top + VELOCITY*direction[1]) % HEIGHT

                if (robot_rect.left % SQUARESIZE == 0) and (robot_rect.top % SQUARESIZE == 0):
                    arrived = True
                    waiting = WAITING
                    robot_idx += 1

                draw_nice_rect(screen, WIDTH, HEIGHT, ROBOT_COLOUR, robot_rect)

        pygame.display.flip()