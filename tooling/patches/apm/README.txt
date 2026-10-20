APM Claude command frontmatter fix
=================================

claude-command-frontmatter.patch preserves the local APM fix associated
with https://github.com/microsoft/apm/issues/3067.

Upstream repository: https://github.com/microsoft/apm
Base commit: 8974961
Patch commit: ad64727
License: MIT; see LICENSE.apm in this directory.

This is a stored source patch, not an installed APM upgrade. Pack installs
and CI do not automatically apply it. It preserves Claude-native command
frontmatter, retains other targets' conversion behavior, and gates command
hooks through APM's existing package hook approval.

To apply, use a separate APM checkout at the base commit, with a clean
working tree:

    git apply --check <absolute-path-to-claude-command-frontmatter.patch>
    git am <absolute-path-to-claude-command-frontmatter.patch>

The upstream patch was locally validated on Windows with Python 3.12.13:
321 focused tests passed; Ruff lint and formatting checks passed.
This does not establish compatibility with newer upstream commits or prove
the behavior of an installed APM release. Review and retest before use.

No upstream push succeeded. Applying or installing this patch is a separate
operation; keeping it here only preserves the work for future maintenance.
