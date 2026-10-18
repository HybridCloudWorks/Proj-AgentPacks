# Design Decisions

1. Use a thin Archivist router and 18 focused Skills to reduce duplicated documentation guidance.
2. Use reader purpose and Diátaxis classification to prevent mixed-mode documents.
3. Include templates as portable assets and keep them separate from native GitHub issue or PR files.
4. Make truthfulness, source traceability, owner, lifecycle, freshness, and verification part of the documentation contract.
5. Keep publication and connector writes approval-gated; local inventory and validation are safe by default.
6. Generate four vendor targets from one canonical source and validate Skill parity.
7. Use uppercase `VALIDATION_REPORT.md` as the only validation-report filename.

## Gap fill 2026-10-18

This fill added the missing `.apm/prompts/` and `examples/`, along with the templates the workflows produce but the library lacked. The agent, Skills, contract instruction, `apm.yml` and `compatibility/tool-permissions.yml` were not changed. No question could be asked during the fill, so the assumptions below were made.

1. **Eleven prompts, one per primary workflow.** The workflows come from the routing list in `documentation-archivist-orchestration`. Routes that serve one reader outcome share a prompt:
   - style, validation, redaction and hooks go into `review-documentation`;
   - governance, taxonomy and template authoring go into `govern-documentation`;
   - docs-as-code and knowledge-base capture go into `prepare-publication`.

   That is one more than the usual ten. Merging architecture explanation with decision records would have blurred the ADR Skill's one-decision-per-record rule.
2. **Meaning of the five recommendations.** The contract lists them without definitions. Assumed meanings:
   - DOCUMENTATION_READY: complete, checked locally and traced.
   - REVIEW_REQUIRED: complete, but a named person must accept it.
   - CHANGES_REQUIRED: a review found defects.
   - BLOCKED_ON_SOURCE_OR_OWNER: a source, owner, destination or authorization is missing.
   - NOT_VERIFIED: key claims or procedures are unchecked.

   They are written into the new completion-report template, a pack document. The contract instruction is frozen. Prompts name a typical recommendation only where the meaning is unambiguous.
3. **Four templates added.** `completion-report.md`, `handoff.md`, `documentation-plan.md` and `source-ledger.md`. The brief listed only examples and prompts as missing, but the contract and the purpose, research and publishing Skills require these outputs and the library had none of them. The 21 existing templates are unchanged.
4. **Handoff means handoff to a person.** The pack has no specialist agents, so the handoff template is for passing work to an owner, decider or publisher, including external actions that await authorization.
5. **Prompts reference only installed content.** They name Skills and the `cloud-documentation-archivist-contract` instruction. They refer to templates by content type, never by path, because the template folder is not installed.
6. **Examples are synthetic and avoid live vendor facts.** The web was not used. The research example describes vendor behaviour only at the level its supplied exports support, and labels that behaviour not verified. Together the seven examples cover all five recommendations; the publication example is the blocked case.
7. **No `docs/SKILL_INVENTORY.md`.** The file did not exist, and the fill rules allow creating only `docs/PROMPT_INVENTORY.md`. The Skill-to-prompt mapping is in `docs/PROMPT_INVENTORY.md` and `tests/capability-coverage.yml`.
8. **Test metadata.**
   - `tests/capability-coverage.yml` gained a `requirements` list with one entry per Skill, which the shared validator checks. Its existing positive and negative cases are kept and now name their prompt.
   - `tests/trigger-cases.yml` names a prompt for every case and adds six cases and four negative cases.
9. **README.** The stale build commands are replaced: they pointed to a pack-local `build_pack.py` and a `--write-report` flag, neither of which exists. They now use the shared root tooling. Prompt, example and template sections were added. The primary-downloads list was left unchanged and was not verified.
10. **Prompt install behaviour.** `docs/PROMPT_INVENTORY.md` states only what the verified APM notes say. The shared validator's scratch install passed, but the files generated for Gemini CLI and Kiro were not inspected.

Known gaps this fill could not close, because the files are frozen:

- `templates-and-content-models` tells the model to load from the pack's template folder, which APM does not install.
- The contract instruction's description mentions handoff rules, but its body defines none.
