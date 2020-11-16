"""
Monte Carlo simulations to estimate the average number of trials it takes
for a specific condition to be met.

The code here was written with the recursive paradigm in mind, taking that
to a ridiculous extent.

For example, it takes
    ~3.8 dice rolls in order to exist a subset of them that sums to 7.
    4 (?!) dice rolls in order to exist a subset of them that sums to 10.
    7 (?!) dice rolls in order to exist two equal consecutive rolls.
"""

import random, sys

class MCSimulation:
    def __init__(self, experiment, predicate):
        self.experiment = experiment
        self.predicate = predicate

    def estimate_average_length(self, runs):
        lengths = repeat(self.run_until_predicate, runs)
        s = sum_(lengths)
        return s/len_(lengths)

    def run_until_predicate(self, history=None):
        """Runs the experiment until the predicate is verified."""

        if history is None:
            history = []

        if self.predicate(history):
            return history
        else:
            history.append(self.experiment.trial())
            return self.run_until_predicate(history)

class Experiment:
    """Abstract base class for experiments."""
    def __init__(self):
        pass

    def trial(self):
        pass

class DiceRoll(Experiment):
    """Experiment associated with rolling a uniform, n-sided dice."""

    def __init__(self, sides):
        self.sides = sides
        self.p = 1/self.sides

    def trial(self):
        """Rolls a random side of the dice."""
        return self.side_rolled(random.random())

    def side_rolled(self, rnd):
        """Finds the side rolled with a "roulette wheel" approach."""
        if rnd < self.p:
            return 1
        else:
            return 1 + self.side_rolled(rnd - self.p)

def repeat(f, n, history=None):
    """Runs f n times and collects the results in a list."""

    if history is None:
        history = []

    if not n:
        return history
    else:
        outcome = f()
        history = repeat(f, n - 1, history)
        history.append(len_(outcome))
        return history

def len_(l):
    """Returns the length of l."""
    if not l:
        return 0
    else:
        return 1 + len_(l[1:])

def sum_(l):
    """Returns the sum of l."""
    if not l:
        return 0
    else:
        return l[0] + sum_(l[1:])

def exists_subset_sum(l, s):
    """Returns True if a subset of l sums up to s."""
    if not s:
        return True
    if not l:
        return False
    return exists_subset_sum(l[1:], s-l[0]) or exists_subset_sum(l[1:], s)

def all_equal(l):
    """Returns True if all elements of l are equal."""
    if len_(l) < 2:
        return True
    else:
        return l[0] == l[1] and all_equal(l[1:])

def equal_consecutive(l, n):
    """Returns True if there are n consecutive equal elements in l."""
    if len_(l) < n:
        return False
    else:
        return all_equal(l[:n]) or equal_consecutive(l[1:], n)

if __name__ == "__main__":
    N = 900
    # sums_to_ten = lambda l: exists_subset_sum(l, 10)
    # sim = MCSimulation(DiceRoll(6), sums_to_ten)
    sums_to_seven = lambda l: exists_subset_sum(l, 7)
    sim = MCSimulation(DiceRoll(6), sums_to_seven)
    # two_consecutive = lambda l: equal_consecutive(l, 2)
    # sim = MCSimulation(DiceRoll(6), two_consecutive)
    print(sim.estimate_average_length(N))
