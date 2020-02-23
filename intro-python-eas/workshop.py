"""
This file uses the components in components.py to implement a simple genetic algorithm
to evolve a simple robot that cleans a room.
"""

def generate_robot(length):
    """Generate a random robot with the given length."""

    dirs = [Directions.LEFT, Directions.RIGHT, Directions.UP, Directions.DOWN]
    robot = [choice(dirs) for _ in range(length)]
    return robot

if __name__ == "__main__":
    pass