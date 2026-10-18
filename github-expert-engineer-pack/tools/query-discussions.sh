#!/usr/bin/env bash
set -euo pipefail
repo=""; limit=30
while (($#)); do case "$1" in --repo) repo="$2"; shift 2;; --limit) limit="$2"; shift 2;; *) echo "usage: query-discussions.sh [--repo OWNER/REPO] [--limit N]" >&2; exit 2;; esac; done
args=(--limit "$limit" --json number,title,author,createdAt,updatedAt,category,labels,answer,url)
[[ -n "$repo" ]] && args+=(--repo "$repo")
gh discussion list "${args[@]}" | jq '{items: ., item_count: length}'
