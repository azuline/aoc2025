import re
from pathlib import Path

id_ranges = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""
with Path("inputs/02.txt").open("r") as fp:
    id_ranges = fp.read()

result = 0

# Parsing
id_ranges_list = []
for x in re.split(r"\s*,", id_ranges):
    low, high = x.split("-")
    id_ranges_list.append((int(low), int(high)))

# for low, high in id_ranges_list:
#     end = False
#     for num in range(low, high + 1):
#         num_s = str(num)
#         half = len(num_s) // 2
#         part1 = num_s[0:half]
#         part2 = num_s[half:]
#         if part1 == part2:
#             result += num

# Checking
for low, high in id_ranges_list:
    end = False
    for num in range(low, high + 1):
        num_s = str(num)
        for i in range(1, len(num_s) // 2 + 1):
            if len(num_s) % i != 0:
                continue
            substrs = [
                num_s[i * rounds : i * (rounds + 1)]
                for rounds in range(len(num_s) // i)
            ]
            if len(set(substrs)) == 1:
                result += num
                print(f"{num=} {substrs=}")
                break

    print(f"{low=} {high=} {result=}")

print(result)
