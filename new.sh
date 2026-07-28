#!/bin/bash
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

RED=$(tput setaf 1 2>/dev/null || true)
YELLOW=$(tput setaf 3 2>/dev/null || true)
DIM=$(tput dim 2>/dev/null || true)
RESET=$(tput sgr0 2>/dev/null || true)

err() { echo "${RED}✗${RESET} $1"; }

if [ ! -f _template.tex ]; then
  err "No _template.tex found in project root."
  exit 1
fi

if [ -f scratch.tex ] && ! diff -q scratch.tex _template.tex >/dev/null 2>&1; then
  echo "${YELLOW}scratch.tex has content that hasn't been archived by done.sh.${RESET}"
  read -rp "Overwrite anyway? [y/N]: " confirm
  if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    err "Aborted. Run done.sh first if you want to keep this work."
    exit 1
  fi
fi

cp _template.tex scratch.tex
echo "${DIM}scratch.tex reset from _template.tex${RESET}"
