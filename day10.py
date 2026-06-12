from pathlib import Path
import functools
import operator
import re
import dataclasses
import z3

inputstr = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
with Path("inputs/10.txt").open("r") as fp:
    inputstr = fp.read()


@dataclasses.dataclass
class Indicator:
    target: list[bool]
    buttons: list[list[bool]]
    joltage: list[int]
    raw: str


indicators: list[Indicator] = []
for line in inputstr.splitlines():
    m = re.match(r"\[([.#]+)\] \(([^}]+)\) {(.*)}$", line)
    assert m is not None
    target = [c == "#" for c in m[1]]
    buttons_raw = [tuple(int(n) for n in grp.split(",")) for grp in m[2].split(") (")]
    buttonwirings = [[i in idxs for i in range(len(target))] for idxs in buttons_raw]
    joltage = [int(n) for n in m[3].split(",")]
    indicators.append(Indicator(target=target, buttons=buttonwirings, joltage=joltage, raw=line))

# Okay lol... this is a fun problem. This smells just like boolean satisfiability. I'm pretty sure
# this is a constraint solver problem but I don't know how to use those because my work has never
# touched it... should be possible to brute force it tho? Or it's time to learn z3.

# z3!

total = 0
for step in indicators:
    solver = z3.Optimize()
    # Each of the button wirings is a boolean for whether we press it or not. In the problem
    # statement, it didn't say we can't press a button twice, but that ends up being a no op, so
    # each button can be pressed at most once.
    buttonwirings = [z3.Bool(f"button_{i}") for i in range(len(step.buttons))]
    # Create the boolean expression. It is basically:
    #
    #     light1 == light2 == light3 == ...
    #
    # Where each light is XOR union of the button wirings linked up to it...
    for i, amount in enumerate(step.target):
        # Get the buttons that toggle each light:
        connected_buttons = [buttonwirings[j] for j, wiring in enumerate(step.buttons) if wiring[i]]
        chain = functools.reduce(operator.xor, connected_buttons, z3.BoolVal(False))
        solver.add(chain == amount)
    # The number of presses is the number of activated button wirings.
    total_presses = z3.Sum([z3.If(b, 1, 0) for b in buttonwirings])
    # And we want to minimize that.
    solver.minimize(total_presses)
    # Sanity check to make sure that the equation is satisfiable; this is given as a precondition
    # but maybe we wrote a big.
    assert solver.check() == z3.sat
    # Run the solver.
    presses = solver.model().eval(total_presses).as_long()
    # print(f"solving for {presses=} {step.raw=}")
    total += presses

print("Part 1:", total)

total = 0
for step in indicators:
    solver = z3.Optimize()
    # Unlike last time, a button is pressed zero or more times...
    buttonwirings = [z3.Int(f"button_{i}") for i in range(len(step.buttons))]
    for b in buttonwirings:
        solver.add(b >= 0)
    # Instead of a boolean expression, we have:
    #
    #     joltage = light1 + light2 + light3 + ...
    #
    # Where each light is sum of the button wirings linked up to it...
    for i, amount in enumerate(step.joltage):
        # Get the buttons that toggle each light:
        connected_buttons = [buttonwirings[j] for j, wiring in enumerate(step.buttons) if wiring[i]]
        solver.add(z3.Sum(connected_buttons) == amount)
    total_presses = z3.Sum(buttonwirings)
    solver.minimize(total_presses)
    assert solver.check() == z3.sat
    presses = solver.model().eval(total_presses).as_long()
    # print(f"solving for {presses=} {step.raw=}")
    total += presses
print("Part 2:", total)
