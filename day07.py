from pathlib import Path
from collections import Counter

inputstr = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
with Path("inputs/07.txt").open("r") as fp:
    inputstr = fp.read()


lines = list(inputstr.splitlines())

firstline, *lines = lines
beams = [firstline.index("S")]
assert beams[0] > 0

# splits = 0
# for row in lines:
#     newbeams = set()
#     for b in beams:
#         if row[b] == "^":
#             newbeams.update([b - 1, b + 1])
#             splits += 1
#         else:
#             newbeams.add(b)
#     beams = list(newbeams)
#     dbgrow = "".join(["|" if i in newbeams else c for i, c in enumerate(row)])
#     print(f"{dbgrow=} {splits=}")
# print(splits)

beams = Counter(**{str(firstline.index("S")): 1})
for row in lines:
    newbeams = Counter()
    for b, count in beams.items():
        b = int(b)
        if row[b] == "^":
            newbeams[str(b - 1)] += count
            newbeams[str(b + 1)] += count
        else:
            newbeams[str(b)] += count
    beams = newbeams
    dbgrow = "".join(["|" if str(i) in newbeams else c for i, c in enumerate(row)])
    print(f"{dbgrow=} {sum(beams.values())=}")
print(sum(beams.values()))
