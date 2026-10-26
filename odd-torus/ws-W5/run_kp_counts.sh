#!/bin/bash
# Kernel-perfect admissible orientation counts by the old SAT + C-checker code (kernel_torus.py --all).
# Run from odd-torus/: bash ws-W5/run_kp_counts.sh > ws-W5/kp_counts.txt 2> ws-W5/kp_counts_progress.txt
P=/home/sid/work/gt/odd-torus/env/bin/python
for mn in "3 3" "3 5" "3 7" "3 9" "5 5"; do
  echo "=== kernel_torus.py $mn --all"
  /usr/bin/time -f "  wall %es, maxrss %MkB" timeout 7200 $P kernel_torus.py $mn --all | grep -v "^  arcs" 
done
