from pathlib import Path
import itertools

inputstr = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
with Path("inputs/04.txt").open("r") as fp:
    inputstr = fp.read()

# Rows are outer, columns are inner.
diagram = [[x == "@" for x in line] for line in inputstr.splitlines()]
debug = [list(line) for line in inputstr.splitlines()]
eight_directions = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

total = 0
prev_total = None
while total != prev_total:
    prev_total = total
    for x, row in enumerate(diagram):
        for y, paper in enumerate(row):
            if not paper:
                continue
            adjacent_papers = 0
            for x_shift, y_shift in eight_directions:
                x_adj = x + x_shift
                y_adj = y + y_shift
                if (
                    0 <= x_adj < len(diagram)
                    and 0 <= y_adj < len(row)
                    and diagram[x_adj][y_adj]
                ):
                    adjacent_papers += 1
            if adjacent_papers < 4:
                total += 1
                debug[x][y] = "x"
    diagram = [[x == "@" for x in line] for line in debug]
print("\n".join("".join(line) for line in debug))
print(total)
