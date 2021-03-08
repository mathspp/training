"""
Example solution to "Finding a Motif in DNA", from rosalind.info.
"""

from utils import list_to_string

def find(string, motif):
    pos = []
    for i in range(len(string) - len(motif) + 1):
        if string[i:].startswith(motif):
            pos.append(i+1)
    return pos

if __name__ == "__main__":
    print(find("GATATATGCATATACTTATAT", "ATAT"))

    with open("inps/rosalind_subs.txt") as f:
        string, motif = f.read().split()

    print(list_to_string(find(string, motif)))
