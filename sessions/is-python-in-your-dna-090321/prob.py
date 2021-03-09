from collections import Counter
from math import log10

def prob(string, gc_content):
    counts = Counter(string)
    print(counts.most_common(2))
    return (
        (counts["T"] + counts["A"]) * log10((1 - gc_content)/2) +
        (counts["G"] + counts["C"]) * log10(gc_content/2)
    )

print(
    prob("ACGATACAA", 0.129)
)
