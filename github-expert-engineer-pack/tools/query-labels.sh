#!/usr/bin/env bash
set -euo pipefail
owner=""; repo=""; per_page=30; page=1
while (($#)); do case "$1" in --owner) owner="$2"; shift 2;; --repo) repo="$2"; shift 2;; --per-page) per_page="$2"; shift 2;; --page) page="$2"; shift 2;; *) echo "usage: query-labels.sh --owner OWNER --repo REPO [--per-page N] [--page N]" >&2; exit 2;; esac; done
[[ -n "$owner" && -n "$repo" ]] || { echo "owner and repo are required" >&2; exit 2; }
gh api "repos/${owner}/${repo}/labels?per_page=${per_page}&page=${page}" | jq '{items: [.[] | {id,name,color,default,description}], item_count: length}'
