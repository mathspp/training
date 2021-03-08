"""
Example solution to "Consensus and Profile", from rosalind.info.
"""

from collections import Counter
from utils import read_fasta, list_to_string

def profile(symbols, dnas):
    length = len(dnas[0])
    # Chain all dna sequences together.
    chain = "".join(dnas)
    # Empty profile matrix.
    profile = [[0 for _ in range(length)] for _ in range(4)]
    consensus = ""
    for i in range(length):
        c = Counter(chain[i::length])
        for j, symb in enumerate(symbols):
            profile[j][i] = c[symb]
        letter, _ = c.most_common(1)[0]
        consensus += letter
    return consensus, profile

def display(symbols, consensus, profile):
    s = consensus + "\n"
    for symb, counts in zip(symbols, profile):
        s = s + f"{symb}: {list_to_string(counts)}\n"
    return s

if __name__ == "__main__":

    symbols = "ACGT"

    dnas = [
        "ATCCAGCT",
        "GGGCAACT",
        "ATGGATCT",
        "AAGCAACC",
        "TTGGAACT",
        "ATGCCATT",
        "ATGGCACT",
    ]
    display(symbols, *profile(symbols, dnas))

    dnas = read_fasta("inps/rosalind_cons.txt")
    print(dnas)
    s = display(symbols, *profile(symbols, dnas))
    with open("outs/rosalind_cons.txt", "w") as f:
        f.write(s)
