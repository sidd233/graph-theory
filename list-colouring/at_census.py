"""Where is there still room under Alon-Tarsi?

For each graph:  floor = min Delta+ + 1  (Hakimi; no orientation is thinner)
                 AT    = the bound Alon-Tarsi actually achieves
                 chi   = the truth from below (chi <= ch <= AT)
Three outcomes:
  AT = floor             AT is already optimal for this whole family of methods
  AT > floor, chi = AT   AT is forced up correctly; the floor was a FALSE bound
  AT > floor, chi < AT   a genuine gap, and the only place research room can be
"""
from alontarsi import alon_tarsi, min_outdeg
from sweep import classes
from verify_target import chrom
import sys
pc = int.bit_count

n = int(sys.argv[1])
hit = forced = gap = 0
gaps = []
for adj in classes(n):
    E = sum(pc(a) for a in adj) // 2
    if E == 0 or E > int(sys.argv[2]):
        continue
    at, _ = alon_tarsi(adj, n)
    mo = min_outdeg(adj, n) + 1
    x = chrom(adj, n)
    if at == mo:
        hit += 1
    elif x == at:
        forced += 1
    else:
        gap += 1
        gaps.append((adj[:], at, mo, x))
print(f"n={n}: AT = floor in {hit} | AT forced up correctly (chi = AT) in {forced}"
      f" | genuine gap in {gap}")
for adj, at, mo, x in gaps[:8]:
    print(f"    gap: adj={adj} AT={at} floor={mo} chi={x}")
