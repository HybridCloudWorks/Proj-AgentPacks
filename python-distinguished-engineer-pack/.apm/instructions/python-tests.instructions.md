---
description: "Python test design and execution: the repository's runner, isolated fixtures, and unit, contract, integration, property and browser checks matched to risk."
applyTo: "**/test_*.py,**/*_test.py,**/tests/**"
---

# python-tests instructions

Use the repository runner and supported interpreters. Test observable acceptance behavior with isolated fixtures. Match unit/contract/integration/property/browser checks to risk. Cover invalid/auth/timeout/cancellation/duplicate/partial-failure paths as applicable. Never weaken assertions or alter expected behavior simply to pass. Record commands, exit status, skips, environment and what mocks cannot establish. Shared/live/cost-bearing test work requires authority for its exact targets.
