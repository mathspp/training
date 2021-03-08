"""
Example solution to "Speeding Up Motif Finding", from rosalind.info.
"""

from utils import read_fasta, list_to_string

def failure(s):
    r = [0]
    for k in range(1, len(s)):
        sub = s[:k+1]
        prefix = sub[:r[-1]+1]
        while not sub.endswith(prefix):
            prefix = prefix[:-1]
        r.append(len(prefix))

    return r

def kmp(pattern, s):
    fail = failure(pattern)
    # i points to the character in s we are currently trying to match.
    # j points to the character in pattern we are currently trying to match.
    i = j = 0
    while i < len(s) and j < len(pattern):
        if s[i] == pattern[j]:
            i, j = i + 1, j + 1
        elif j > 0:
            j = fail[j-1]
        else:
            i += 1
    if j == len(pattern):
        print("Pattern found at i = ", str(i))
    else:
        print("None :'(")

if __name__ == "__main__":
    print(failure("CAGCATGGTATCACAGCAGAG"))

    kmp("ABCDABD", "ABC ABCDAB ABCDABCDABDE")
    # data = read_fasta("inps/rosalind_kmp.txt")[0]
    # with open("outs/rosalind_kmp.txt", "w") as f:
    #     f.write(list_to_string(failure(data)))
