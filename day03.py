from pathlib import Path

inputstr = """\
987654321111111
811111111111119
234234234234278
818181911112111"""
with Path("inputs/03.txt").open("r") as fp:
    inputstr = fp.read()

banks = [[int(x) for x in line] for line in inputstr.splitlines()]

total = 0
for bank in banks:
    max_joltage = 0
    digits = ""
    prev_idx = 0
    for idx in range(12):
        options = bank[prev_idx : len(bank) + (-1 * (11 - idx))]
        print(f"{prev_idx=} {options=} {idx=}")
        digit_val = max(options)
        prev_idx = options.index(digit_val) + prev_idx + 1
        digits += str(digit_val)
    total += int(digits)
    print(f"{''.join(str(c) for c in bank)=} {digits=}")
print(total)
