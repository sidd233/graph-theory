#!/bin/bash
# Kill lazy_choos jobs (10-vertex first) if available memory falls below 1.5 GB.
while pgrep -f "lazy_choos.py data" >/dev/null; do
  avail=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
  if [ "$avail" -lt 1500 ]; then
    for pid in 11232 11226; do
      if kill -0 $pid 2>/dev/null; then kill $pid; echo "$(date +%I:%M%p) killed $pid, avail=${avail}MB"; break; fi
    done
  fi
  sleep 3
done
echo "$(date +%I:%M%p) no lazy jobs left"
