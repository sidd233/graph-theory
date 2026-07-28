#!/bin/bash
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

BOLD=$(tput bold 2>/dev/null || true)
DIM=$(tput dim 2>/dev/null || true)
RED=$(tput setaf 1 2>/dev/null || true)
GREEN=$(tput setaf 2 2>/dev/null || true)
YELLOW=$(tput setaf 3 2>/dev/null || true)
CYAN=$(tput setaf 6 2>/dev/null || true)
RESET=$(tput sgr0 2>/dev/null || true)

err() { echo "${RED}✗${RESET} $1"; }
ok()  { echo "${GREEN}✓${RESET} $1"; }

if [ ! -f build/scratch.pdf ]; then
  err "No build/scratch.pdf found. Compile scratch.tex first."
  exit 1
fi

if [ ! -f scratch.tex ]; then
  err "No scratch.tex found in project root."
  exit 1
fi

if [ ! -f _template.tex ]; then
  err "No _template.tex found in project root."
  exit 1
fi

mkdir -p notes latex

current=""

while true; do
  base="notes"
  [ -n "$current" ] && base="notes/$current"

  mapfile -t subs < <(find "$base" -mindepth 1 -maxdepth 1 -type d | sed "s#^$base/##" | sort)

  label="notes/"
  [ -n "$current" ] && label="notes/$current/"

  echo
  echo "${BOLD}${label}${RESET}"
  i=1
  for s in "${subs[@]}"; do
    echo "  ${CYAN}$i${RESET}) $s/"
    i=$((i+1))
  done
  echo "  ${CYAN}.${RESET}) save here"
  echo "  ${CYAN}n${RESET}) new subfolder"
  echo

  read -rp "> " choice

  if [[ "$choice" == "." ]]; then
    target_folder="$current"
    break
  elif [[ "$choice" == "n" || "$choice" == "N" ]]; then
    read -rp "New subfolder name: " newname
    newname="${newname%/}"
    if [ -z "$newname" ]; then
      err "Folder name cannot be empty."
      exit 1
    fi
    if [ -n "$current" ]; then
      current="$current/$newname"
    else
      current="$newname"
    fi
    mkdir -p "notes/$current"
  elif [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "${#subs[@]}" ]; then
    chosen="${subs[$((choice-1))]}"
    if [ -n "$current" ]; then
      current="$current/$chosen"
    else
      current="$chosen"
    fi
  else
    err "Not a valid option, try again."
  fi
done

echo
read -rp "File name (no extension): " filename
if [ -z "$filename" ]; then
  err "Filename cannot be empty."
  exit 1
fi

if [ -n "$target_folder" ]; then
  pdf_dest="notes/$target_folder/$filename.pdf"
  tex_dest="latex/$target_folder/$filename.tex"
else
  pdf_dest="notes/$filename.pdf"
  tex_dest="latex/$filename.tex"
fi

if [ -e "$pdf_dest" ] || [ -e "$tex_dest" ]; then
  echo "${YELLOW}$pdf_dest or $tex_dest already exists.${RESET}"
  read -rp "Overwrite? [y/N]: " overwrite
  if [[ "$overwrite" != "y" && "$overwrite" != "Y" ]]; then
    err "Aborted, nothing was overwritten."
    exit 1
  fi
fi

mkdir -p "$(dirname "$pdf_dest")"
mkdir -p "$(dirname "$tex_dest")"

cp build/scratch.pdf "$pdf_dest"
cp scratch.tex "$tex_dest"

echo
ok "$pdf_dest"
ok "$tex_dest"

cp _template.tex scratch.tex
echo "${DIM}scratch.tex reset from _template.tex${RESET}"

echo
# -----------------------------
# Git
# -----------------------------

echo

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    err "Not inside a Git repository."
    exit 1
fi

# Determine commit scope from destination folder
relative_path="${tex_dest#latex/}"

if [[ "$relative_path" == */* ]]; then
    scope="${relative_path%%/*}"
else
    scope="root"
fi

# Create a slug from the filename
slug=$(echo "$filename" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/ /-/g')

default_msg="docs(${scope}): add ${slug}"

echo "${CYAN}Default commit message:${RESET}"
echo "  $default_msg"
echo

read -rp "Commit message [Press Enter to use default]: " commit_msg
commit_msg=${commit_msg:-$default_msg}

echo
echo "${CYAN}Final commit message:${RESET}"
echo "  $commit_msg"
echo

read -rp "Commit and push? [Y/n]: " confirm
confirm=${confirm:-Y}

if [[ "$confirm" =~ ^[Yy]$ ]]; then

    # Stage only the files related to this note
    git add "$tex_dest"
    git add "$pdf_dest"

    # Stage the reset working file if it exists
    if [ -f scratch.tex ]; then
        git add scratch.tex
    fi

    if [ -f latex/current.tex ]; then
        git add latex/current.tex
    fi

    if git diff --cached --quiet; then
        echo "${YELLOW}Nothing to commit.${RESET}"
        exit 0
    fi
    git commit -m "$commit_msg"
    echo
    echo "${CYAN}Pushing to GitHub...${RESET}"
    git push
    echo
    ok "Changes committed and pushed successfully."

else
    echo "${YELLOW}Skipped Git commit and push.${RESET}"
fi