import math
import pprint
from pathlib import Path

inputstr = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
with Path("inputs/08.txt").open("r") as fp:
    inputstr = fp.read()

# (x,y,z) tuples
junctions = [tuple([int(x) for x in line.split(",")]) for line in inputstr.splitlines()]
assert all(len(t) == 3 for t in junctions)

# inefficient for now who cares; at 1000 input values its only a million loops to do n^2.

# tuple(tuple, tuple) -> number
distances = {}

for i, box1 in enumerate(junctions):
    for box2 in junctions[i + 1 :]:
        distances[box1, box2] = math.sqrt(
            abs(box2[0] - box1[0]) ** 2
            + abs(box2[1] - box1[1]) ** 2
            + abs(box2[2] - box1[2]) ** 2
        )

alld = list(distances.items())
alld.sort(key=lambda x: x[1])

# now we have a graph of nodes with 1000 edges.
# we want to find the three largest subgraphs and then the product of their sizes
# i forget the canonical algo so ill have to study more later but for now just yolo brute force it
# right
#
#
# state:
# - what operations do we want? given two nodes in an edge, find their subgraphs and combine
#   - means: lookup, combination/mutation
# - how to design structure for that?

# subgraphs = [{x} for x in junctions]
# lookup = {next(iter(xs)): xs for xs in subgraphs}

# for (box1, box2), _ in alld[:1000]:
#     # merge box2 to box1
#     sg1 = lookup[box1]
#     sg2 = lookup[box2]
#     if sg1 == sg2:
#         continue
#     subgraphs.remove(sg2)
#     sg1.update(sg2)
#     for b in sg2:
#         lookup[b] = sg1

# subgraphs.sort(key=len)
# subgraphs = subgraphs[-3:]
# pprint.pprint(subgraphs)
# print(math.prod(len(xs) for xs in subgraphs))

subgraphs = [{x} for x in junctions]
lookup = {next(iter(xs)): xs for xs in subgraphs}

for (box1, box2), _ in alld:
    # merge box2 to box1
    sg1 = lookup[box1]
    sg2 = lookup[box2]
    if sg1 == sg2:
        continue
    if len(subgraphs) == 2:
        print(box1[0] * box2[0])
        break
    subgraphs.remove(sg2)
    sg1.update(sg2)
    for b in sg2:
        lookup[b] = sg1
