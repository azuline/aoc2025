import math
from pathlib import Path

inputstr = """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
with Path("inputs/06.txt").open("r") as fp:
    inputstr = fp.read()

rows = list(inputstr.splitlines())

space_cols = set(range(len(rows[0])))
for row in rows:
    space_cols -= {i for i, c in enumerate(row) if c != " "}

space_cols = [0, *sorted(space_cols), len(rows[0])]
splitrows = []
for r in rows:
    splitr = []
    for i in range(len(space_cols) - 1):
        splitr.append(r[space_cols[i] : space_cols[i + 1]])
    splitrows.append(splitr)
del rows, space_cols

pivot = [[] for _ in range(len(splitrows[0]))]
for r in splitrows:
    for i, val in enumerate(r):
        pivot[i].append(val)
del splitrows

total = 0
for eqn in pivot:
    operation, *operands_str = [s for s in eqn[::-1]]
    operation = operation.strip()
    assert operation in ("+", "*")

    # Now we have to pivot the operands...
    width = len(operands_str[0])
    operands = [""] * width
    for i in range(width):
        for o in operands_str[::-1]:
            operands[width - i - 1] += o[i]
    operands = [int(x) for x in operands if x.strip()]

    fn = sum if operation == "+" else math.prod
    chunk = fn(operands)
    total += chunk
    print(f"{total=} {chunk=} {operation=} {operands=}")

print(total)
