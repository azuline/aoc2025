from collections import defaultdict
import functools
from pathlib import Path

# inputstr = """\
# aaa: you hhh
# you: bbb ccc
# bbb: ddd eee
# ccc: ddd eee fff
# ddd: ggg
# eee: out
# fff: out
# ggg: out
# hhh: ccc fff iii
# iii: out"""
inputstr = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""
with Path("inputs/11.txt").open("r") as fp:
    inputstr = fp.read()

nodes = {"out"}
edges = set()
edges_map = defaultdict(list)

for line in inputstr.splitlines():
    src, dsts = line.split(": ", 1)
    nodes.add(src)
    for dst in dsts.split(" "):
        edges.add((src, dst))
        edges_map[src].append(dst)

# Part 1: Pretty sure this is straightforward recursion. DP if optimization is needed. Going to do
# top-down as its simpler and we don't care for perf.

# def count_paths_to_out(node: str) -> int:
#     # Base case.
#     if node == "out":
#         return 1
#     # Recursive case.
#     return sum(count_paths_to_out(dst) for dst in edges_map[node])


# print("Part 1:", len(count_paths_to_out("you")))


@functools.cache
def count_paths_to_dst(node: str, dst: str) -> int:
    # Base case.
    if node == dst:
        return 1
    # Recursive case.
    return sum(count_paths_to_dst(nxt, dst) for nxt in edges_map[node])


# 1. Tried to keep track of the state of visited nodes, but while the time complexity was fine, the
#    space complexity blew up.
# 2. So alternatively, we went back to counting, but increased constant factor by six times while
#    keeping space complexity cheap. Compute the paths piecewise like so:
dac_to_fft = count_paths_to_dst("svr", "dac") * count_paths_to_dst("dac", "fft") * count_paths_to_dst("fft", "out")
fft_to_dac = count_paths_to_dst("svr", "fft") * count_paths_to_dst("fft", "dac") * count_paths_to_dst("dac", "out")
print("Part 2:", dac_to_fft + fft_to_dac)
