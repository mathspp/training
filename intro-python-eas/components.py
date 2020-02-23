import pygame
from pygame.locals import *

from random import random

class Directions(object):
    """Hold the directions in which the robot can walk."""

    LEFT = [-1, 0]
    RIGHT = [1, 0]
    UP = [0, 1]
    DOWN = [0, -1]

def generate_map(width, height):
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

    return score, room_copy

def render_simulation(simulation):
    pass