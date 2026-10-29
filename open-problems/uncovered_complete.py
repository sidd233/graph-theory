"""Even orders n for which the List Edge Colouring Conjecture for K_n is NOT
covered by the known infinite families (status checked 2026-10-07):

  K_{p+1}  Schauz, Electron. J. Combin. 21(3) (2014) P3.43
  K_{p-1}  Jafari, arXiv:2608.22895 (2026), Theorem 1.1
  K_{2p}   Jafari, arXiv:2608.22895 (2026), Theorem 1.2

with p an odd prime. Odd n is settled (Haggkvist and Janssen 1997), and K_2 is trivial.
Run: python3 open-problems/uncovered_complete.py [limit]
"""
import sys


def is_odd_prime(m):
    if m < 3 or m % 2 == 0:
        return False
    d = 3
    while d * d <= m:
        if m % d == 0:
            return False
        d += 2
    return True


def covered(n):
    return is_odd_prime(n - 1) or is_odd_prime(n + 1) or (n % 2 == 0 and is_odd_prime(n // 2))


limit = int(sys.argv[1]) if len(sys.argv) > 1 else 200
open_orders = [n for n in range(4, limit + 1, 2) if not covered(n)]
print(f"even n in [4, {limit}] not covered: {open_orders}")
print(f"smallest: {open_orders[0] if open_orders else None}")
