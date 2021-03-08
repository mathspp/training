"""
Example solution to "Introduction to Random Strings", from rosalind.info.
"""

from math import log10
from utils import list_to_string

def prob(seq, probs):
    """Log10 probability of seq being randomly built with given probabilities."""
    acc = 0
    for symb in seq:
        acc += log10(probs[symb])
    return acc

if __name__ == "__main__":
    print(prob("ACGATACAA", {"A": 0.871/2, "T": 0.871/2, "C": 0.129/2, "G": 0.129/2}))

    with open("inps/rosalind_prob.txt", "r") as f:
        contents = f.read().split("\n")
    dna = contents[0]
    floats = contents[1]

    probs = []
    for s in floats.split(" "):
        f = float(s)
        p, p_ = f/2, (1-f)/2
        d = {"A": p_, "T": p_, "C": p, "G": p}
        probs.append(round(prob(dna, d), 3))
    print(list_to_string(probs))
