# Design Decisions

1. Use a thin `github-expert-engineer` router and 18 focused Skills to limit prompt duplication.
2. Treat GitHub content and AI-generated code as untrusted data and preserve human approval boundaries.
3. Keep query helpers read-only, bounded, schema-first, and explicit about owner/repository and pagination.
4. Make mutation guards and hooks available, but never hide authorization behind a script flag.
5. Generate four vendor targets from one canonical source and validate exact Skill parity.
6. Use uppercase `VALIDATION_REPORT.md` as the only validation-report filename.
7. Record official documentation URLs while separating static pack proof from live GitHub state.
