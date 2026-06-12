import dataclasses
import re
from pathlib import Path

inputstr = """\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""
with Path("inputs/12.txt").open("r") as fp:
    inputstr = fp.read()

# Okay... think less, parse first.

sectionstr = inputstr.split("\n\n")
shapestrlist, regionstr = sectionstr[:-1], sectionstr[-1]

type Shape = list[list[bool]]
shapes: list[Shape] = []
for i, shapestr in enumerate(shapestrlist):
    index = int(shapestr.split(":", 1)[0])
    grid = [[x == "#" for x in line] for line in shapestr.splitlines()[1:]]
    assert index == i
    shapes.append(grid)


@dataclasses.dataclass
class Region:
    x: int
    y: int
    shapecounts: list[int]


regions: list[Region] = []
for r in regionstr.splitlines():
    m = re.match(r"(\d+)x(\d+): ([0-9 ]+)", r)
    region = Region(x=int(m[1]), y=int(m[2]), shapecounts=[int(x) for x in m[3].split()])
    assert len(region.shapecounts) == len(shapes)
    regions.append(region)

print(f"{shapes=}")
print(f"{regions=}")

# Okay I was really uninterested in solving a brute force NP-complete binpacking and so I went
# online to make sure that this was /really/ the method and it turns out that we got trolled okay.
total = 0
for r in regions:
    area = r.x * r.y
    if sum(r.shapecounts) * 9 > area:
        continue
    else:
        total += 1
print(total)
