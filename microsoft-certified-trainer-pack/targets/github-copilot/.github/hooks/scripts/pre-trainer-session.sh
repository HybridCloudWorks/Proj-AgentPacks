#!/usr/bin/env bash
set -eu
printf '%s\n' 'Trainer preflight: inspect course sources, audience, duration, permissions, licensing, accessibility, and environment before authoring or delivering.'
if [ -f DESCRIPTION.md ]; then printf '%s\n' 'Trainer pack detected.'; fi
if [ -f VALIDATION_REPORT.md ]; then printf '%s\n' 'Existing validation report is reference only; rebuild after changes.'; fi
