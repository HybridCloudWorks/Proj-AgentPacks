# Completion report

The pack's always-on `azure-expert-designer-contract` instruction defines the nine sections and seven evidence labels. Use the section names as headings, in this order, and end each fact or check with exactly one evidence label.

Evidence labels:

- `observed`: present in the supplied source, file or evidence.
- `inferred`: derived from the evidence, not stated by it.
- `designed`: a design choice with no source behind it.
- `structurally-validated`: a static check of the file was executed and passed.
- `visually-validated`: the actual rendered output was opened or exported and inspected.
- `live-verified`: checked against a live Azure environment with approved access.
- `not-verified`: not checked. Say why.

Never describe an unexecuted check as passed. Static XML checks are never visual validation, and neither is evidence of a deployed or secure Azure system.

---

## Completion report

Pack: azure-expert-designer.

### scope_and_inputs

- Task type and outcome:
- Request, purpose and audience:
- Inputs used, with paths and commit:
- Approvals in effect, and their scope:

### source_facts

- Fact, with file and resource or requirement reference. `observed`

### assumptions_and_design_decisions

- Assumption or decision, and its effect if wrong. `inferred` or `designed`

### output_files

- Path, and what it is. Say "none" when nothing was written, and name any file that was deliberately left unchanged.

### structural_checks

- Check, command or method, and result. `structurally-validated` or `not-verified`

### visual_checks

- Renderer path and version, pages and size inspected, defects found and fixed. `visually-validated` or `not-verified`

### live_or_external_checks

- Live Azure, CLI or external system checked, and the approval used. `live-verified` or `not-verified`

### unresolved_risks

- Risk, why it is open, and what evidence would close it.

### next_safe_action

- The single next step that is safe to take, and who must take it.
