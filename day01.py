from typing import Literal
from pathlib import Path


rotations = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
with Path("inputs/01.txt").open("r") as fp:
    rotations = fp.read()

lock = 50
zeroes = 0

# for move in rotations.splitlines():
#     direction: Literal["L", "R"] = move[0]
#     assert direction in ("L", "R")
#     magnitude = int(move[1:])
#     if direction == "L":
#         magnitude *= -1

#     lock += magnitude
#     lock = lock % 100
#     if lock == 0:
#         zeroes += 1

#     print(f"{move=} {lock=} {zeroes=}")

for move in rotations.splitlines():
    direction: Literal["L", "R"] = move[0]
    assert direction in ("L", "R")
    magnitude = int(move[1:])

    step = 1 if direction == "R" else -1

    for _ in range(magnitude):
        lock = (lock + step) % 100
        if lock == 0:
            zeroes += 1

    print(f"{move=} {lock=} {zeroes=}")

print(zeroes)
