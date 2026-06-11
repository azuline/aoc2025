from pathlib import Path
import dataclasses

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


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int


tiles = [Point(*[int(x) for x in line.split(",")]) for line in inputstr.splitlines()]

# max_seen = 0
# for i, t1 in enumerate(tiles):
#     for t2 in tiles[i + 1 :]:
#         size = (abs(t2.x - t1.x) + 1) * (abs(t2.y - t1.y) + 1)
#         max_seen = max(max_seen, size)


# shrink
min_x = min(t.x for t in tiles)
min_y = min(t.y for t in tiles)
red_tiles = tiles  # [Point(x=t.x - min_x, y=t.y - min_y) for t in tiles]
del tiles

green_tiles = set()
for i in range(len(red_tiles) - 1):
    t1, t2 = red_tiles[i], red_tiles[i + 1]
    # Go off horizontal/vertical:
    if t1.x == t2.x:
        ylow, yhigh = (t1.y, t2.y) if t1.y <= t2.y else (t2.y, t1.y)
        for y in range(ylow + 1, yhigh):
            green_tiles.add(Point(x=t1.x, y=y))
    else:
        xlow, xhigh = (t1.x, t2.x) if t1.x <= t2.x else (t2.x, t1.x)
        for x in range(xlow + 1, xhigh):
            green_tiles.add(Point(x=x, y=t1.y))
del t1, t2

tiles = [*red_tiles, *green_tiles]
tiles_set = {*red_tiles, *green_tiles}

# Useful for the below logic for perf. For every x and y axis, we store the min/max of the other
# axis tiles.
tiles_boundaries_x_miny = {}
tiles_boundaries_x_maxy = {}
tiles_boundaries_y_minx = {}
tiles_boundaries_y_maxx = {}
for t in tiles:
    tiles_boundaries_x_miny[t.x] = min(tiles_boundaries_x_miny.get(t.x, 999999), t.y)
    tiles_boundaries_x_maxy[t.x] = max(tiles_boundaries_x_maxy.get(t.x, -1), t.y)
    tiles_boundaries_y_minx[t.y] = min(tiles_boundaries_y_minx.get(t.y, 999999), t.x)
    tiles_boundaries_y_maxx[t.y] = max(tiles_boundaries_y_maxx.get(t.y, -1), t.x)

max_seen = 0
for i, t1_dontuse in enumerate(red_tiles):
    for t2_dontuse in red_tiles[i + 1 :]:
        valid = True

        # Okay our logic here is: start at the left corner and then trace right. We want to make
        # sure that for any tile on the path that exists before we reach the other side, we never
        # have the edge go in the vertical direction. At the very end, we must either meet a tile or
        # there must a tile somewhere in the direction.
        #
        # Then we go up and repeat, tracing each side this way.
        #
        # The implicit definition here of validity is:
        #
        # 1. We check to see that the rectangle is on the "inside" of our big shape by checking to
        # see that if the line extends, it would eventually intersect.
        # 2. We check to see that the rectangle does not exceed our big shape by looking for areas
        # where the big shape would cross over our rectangle.
        #
        # I believe these two are exhaustive...
        #
        # Takes forever, but if I optimize I'm probably going to introduce bugs... there are def
        # more efficient structures for the tracing that we can precompute once. We are using 1d
        # structures for a 2d problem.
        tleft, tright = (
            (t1_dontuse, t2_dontuse)
            if t1_dontuse.x < t2_dontuse.x
            else (t2_dontuse, t1_dontuse)
        )
        tdown, tup = (
            (t1_dontuse, t2_dontuse)
            if t1_dontuse.y < t2_dontuse.y
            else (t2_dontuse, t1_dontuse)
        )
        # +1 for up, -1 for down
        direction_x = 1 if tright.y - tleft.y > 0 else -1
        # +1 for right, -1 for left
        direction_y = 1 if tup.x - tdown.x > 0 else -1

        size = (abs(tright.x - tleft.x) + 1) * (abs(tright.y - tleft.y) + 1)
        # don't bother.
        if size < max_seen:
            print(f"{tleft=} {tright=} skipped b/c size too small")
            continue

        # First check condition 1 of validity for all edges.
        assert tiles_boundaries_y_maxx[tleft.y] >= tleft.x
        assert tiles_boundaries_y_minx[tright.y] <= tright.x
        assert tiles_boundaries_x_maxy[tdown.x] >= tdown.y
        assert tiles_boundaries_x_miny[tup.x] <= tup.y
        if (
            tiles_boundaries_y_maxx[tleft.y] == tleft.x
            or tiles_boundaries_y_minx[tright.y] == tright.x
            or tiles_boundaries_x_maxy[tdown.x] == tdown.y
            or tiles_boundaries_x_miny[tup.x] == tup.y
        ):
            print(f"{tleft=} {tright=} failed boundary check 1")
            valid = False
            continue

        # Then check condition 2. We'll just step in four directions.

        # 1. L->R and R->L
        for x in range(tleft.x + 1, tright.x):
            if (
                Point(x=x, y=tleft.y) in tiles_set
                and Point(x=x, y=tleft.y + direction_x) in tiles_set
            ):
                valid = False
                break
            if (
                Point(x=x, y=tright.y) in tiles_set
                and Point(x=x, y=tright.y - direction_x) in tiles_set
            ):
                valid = False
                break
        if not valid:
            print(f"{tleft=} {tright=} failed boundary check 2 on L->R / R->L")
            continue

        for y in range(tdown.y + 1, tup.y):
            if (
                Point(x=tdown.x, y=y) in tiles_set
                and Point(x=tdown.x + direction_y, y=y) in tiles_set
            ):
                valid = False
                break
            if (
                Point(x=tup.x, y=y) in tiles_set
                and Point(x=tup.x - direction_y, y=y) in tiles_set
            ):
                valid = False
                break
        if not valid:
            print(f"{tleft=} {tright=} failed boundary check 2 on D->U / U->D")
            continue

        print(f"{tleft=} {tright=} {size=} valid")
        max_seen = max(max_seen, size)

print(max_seen)
