from pathlib import Path

inputstr = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
with Path("inputs/09.txt").open("r") as fp:
    inputstr = fp.read()

tiles = [tuple([int(x) for x in line.split(",")]) for line in inputstr.splitlines()]
assert all(len(t) == 2 for t in tiles)

# max_seen = 0
# for i, t1 in enumerate(tiles):
#     for t2 in tiles[i + 1 :]:
#         size = (abs(t2[0] - t1[0]) + 1) * (abs(t2[1] - t1[1]) + 1)
#         max_seen = max(max_seen, size)


# shrink
min_x = min(t[0] for t in tiles)
min_y = min(t[1] for t in tiles)
tiles = [(x - min_x, y - min_y) for x, y in tiles]

# a bit too lazy to do this, brute force is:
#
# 1. get all edges of the shape
# 2. fill in a set of all tiles by scanning each 'x' and getting valid 'y's.
# 3. for all rectangles, use set diff
#
# slow but can terminate in a reasonable timeframe given our input size
#
# this is way too slow, but the alternative of working on the edges alone has so many edge cases
# that complicate it.
