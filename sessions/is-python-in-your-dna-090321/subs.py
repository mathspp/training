def subs(string, pattern):
    results = []
    pattern_length = len(pattern)
    for start_slice in range(len(string)):
        slice_ = string[start_slice:start_slice + pattern_length]
        if slice_ == pattern:
            results.append(start_slice + 1)

    return results

print(
    subs("GATATATGCATATACTT", "ATAT")
)
