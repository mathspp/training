"""
Utility functions to solve problems from rosalind.info.
"""

def read_fasta(file, remove_headers=True):
    """Reads DNA strings from a file in FASTA format."""
    with open(file) as f:
        contents = [line[:-1] for line in f.readlines()]

    data = []
    header = contents[0]
    dna = ""
    for line in contents[1:] + [">"]:
        if line.startswith(">"):
            if remove_headers:
                data.append(dna)
            else:
                data.append((header, dna))
            dna = ""
            header = line[1:]
        else:
            dna = dna + line

    return data

def list_to_string(l):
    return " ".join(map(str, l))
