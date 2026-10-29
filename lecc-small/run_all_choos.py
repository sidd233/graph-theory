"""Run the pruned choosability search (choosability.py --reduce) on every open zero-sum graph.

Output: data/choos_all.csv (graph6, N, k, result, seconds, iterations line); logs in
data/choos_logs/. Runs graphs in parallel worker processes, each with its own time limit.
Run: env/bin/python run_all_choos.py [workers] [time_limit_seconds]
"""
import csv
import os
import sys
import time
from multiprocessing import Pool

import networkx as nx

from choosability import search



def job(arg):
    g6, limit = arg
    G = nx.from_graph6_bytes(g6.encode())
    k = max(d for _, d in G.degree())
    H = nx.line_graph(G)
    msgs = []
    t = time.time()
    res, _ = search(H, k, log=msgs.append, time_limit=limit, reduce=True)
    safe = g6.replace("/", "_").replace("\\", "_")
    with open(os.path.join("data/choos_logs", safe + ".log"), "w") as f:
        f.write("\n".join(msgs) + "\n")
    return [g6, G.number_of_nodes(), k, res, round(time.time() - t, 1), msgs[-1]]


if __name__ == "__main__":
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    limit = float(sys.argv[2]) if len(sys.argv) > 2 else 1200
    os.makedirs("data/choos_logs", exist_ok=True)
    graphs = [l.strip() for f in ("data/uncovered_N8.g6", "data/uncovered_N10.g6")
              for l in open(f) if l.strip()]
    with open("data/choos_all.csv", "w", newline="") as out:
        w = csv.writer(out)
        w.writerow(["graph6", "N", "k", "result", "seconds", "last_log"])
        with Pool(workers) as pool:
            for row in pool.imap_unordered(job, [(g, limit) for g in graphs]):
                w.writerow(row)
                out.flush()
                print(row[:5], flush=True)
