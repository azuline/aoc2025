from pathlib import Path

inputstr = """\
3-5
10-14
16-20
12-18
9-21

1
5
8
11
17
32"""
with Path("inputs/05.txt").open("r") as fp:
    inputstr = fp.read()

freshness_str, eval_str = inputstr.split("\n\n")

freshness_ranges = []
for line in freshness_str.splitlines():
    low, high = line.split("-")
    freshness_ranges.append((int(low), int(high), False))

# ingredients = [int(x) for x in eval_str.splitlines()]

# total = 0
# for ing in ingredients:
#     for low, high, _ in freshness_ranges:
#         if low <= ing <= high:
#             total += 1
#             break
# print(total)

# THOUGHT:
#
# Restating the problem, we have ranges r_1 to r_N and we want to ensure that none are overlapping.
#
# Definition of overlapping: given two ranges r1 and r2, WLOG (r1.low <= r2.low)
#   Is Overlapping = r1.high >= r2.low
#
# Types of Overlapping (twofold):
# 1. r1.high < r2.high
# 2. r1.high >= r2.high
#
# How to massage the ranges to prevent overlapping:
# 1. r1.high < r2.high -> set r1.high to be r2.low - 1
# 2. r1.high >= r2.high -> delete r2
#
# And we can do this n^2.
#
# Is mutation safe?
#
# I think so. We never mutate the low so we never violate wlog property. Any other properties
# matter? I don't think so.

# Sort by low to maintain wlog property for r1 and r2.
freshness_ranges.sort(key=lambda x: x[0])

for i, (r1_low, r1_high, deleted) in enumerate(freshness_ranges):
    if deleted:
        continue
    for j, (r2_low, r2_high, deleted) in enumerate(freshness_ranges[i + 1 :]):
        if deleted:
            continue
        assert r1_low <= r2_low
        if r1_high >= r2_low:
            if r1_high < r2_high:
                r1_high = r2_low - 1
                freshness_ranges[i] = (r1_low, r1_high, False)
            else:
                freshness_ranges[i + j + 1] = (r2_low, r2_high, True)

print(freshness_ranges)

total = 0
for i, (r1_low, r1_high, deleted) in enumerate(freshness_ranges):
    if not deleted:
        total += r1_high - r1_low + 1
print(total)
