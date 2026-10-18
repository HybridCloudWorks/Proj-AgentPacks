#!/usr/bin/env bash
set -euo pipefail
repo=""; state="open"; limit=30
while (($#)); do case "$1" in --repo) repo="$2"; shift 2;; --state) state="$2"; shift 2;; --limit) limit="$2"; shift 2;; *) echo "usage: query-issues.sh [--repo OWNER/REPO] [--state open|closed|all] [--limit N]" >&2; exit 2;; esac; done
args=(--state "$state" --limit "$limit" --json number,title,state,author,createdAt,updatedAt,labels,assignees,url)
[[ -n "$repo" ]] && args+=(--repo "$repo")
gh issue list "${args[@]}" | jq '{items: ., item_count: length}'
