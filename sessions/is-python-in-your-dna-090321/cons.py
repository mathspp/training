from collections import Counter

def profile(strings, symbols):
    if not strings:
        return None

    profile_matrix = []
    dna = "".join(strings)
    jump = len(strings[0])
    for col in range(len(strings[0])):
        column = dna[col::jump]
        counts = Counter(column)
        # # List comprehensions are Pythonic
        # count_list = [counts[symb] for symb in symbols]
        count_list = []
        for symb in symbols:
            count_list.append(counts[symb])
        profile_matrix.append(count_list)

    return profile_matrix

def consensus(profile_matrix, symbols):
    consensus = ""
    for count_list in profile_matrix:
        m = max(count_list)
        max_pos = count_list.index(m)
        consensus = consensus + symbols[max_pos]
    return consensus

dnas = [
    "ATCCAGCT",
    "GGGCAACT",
    "ATGGATCT",
    "AAGCAACC",
    "TTGGAACT",
    "ATGCCATT",
    "ATGGCACT",
]

print(
    profile(dnas, "ACGT")
)
