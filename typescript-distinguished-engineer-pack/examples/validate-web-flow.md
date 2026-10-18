# Worked example — team invitation journey in a React admin app

| | |
|---|---|
| Workflow | `.apm/prompts/validate-web-flow.prompt.md` |
| Primary agent | `typescript-distinguished-engineer` |
| Specialist | `typescript-test-engineer` |
| Skills | `playwright-validation`, `frontend-react-engineering`, `layered-testing-and-test-engineering`, `api-contract-and-integration-engineering` |
| Outcome | `COMPLETE_VERIFIED` for the configured browser projects against the local mock API |

> Synthetic walkthrough. The repository, paths, commands and output are illustrative. They show the shape of the workflow and are not evidence from a real run; never reuse them as a completion claim.

## Request

"Before we release the new invitations screen in `admin-web`, verify the invite journey end to end, error cases included. Fix what's broken."

The user authorizes local edits and local test runs. The journey runs only against the repository's local preview server and mock API.

## Perceive

`playwright-validation` inspects what exists before writing a locator.

- `apps/admin-web` is a React and Vite single-page app. Screens live in `src/features/`; mutations go through the app's `useMutation` wrapper around `src/api/`.
- `playwright.config.ts`:
  - Projects: `chromium` and `firefox`.
  - `webServer` runs `pnpm preview` against the mock API in `mocks/`.
  - Diagnostics: `trace: "retain-on-failure"` and `screenshot: "only-on-failure"`.
  - Global setup signs in a synthetic owner and a synthetic member through the mock auth and writes their storage state to `playwright/.auth/`.
- `git check-ignore -v playwright/.auth/owner.json` confirms the storage-state files are ignored. `test-results/` is ignored too.
- `@axe-core/playwright` is already a dev dependency, used by two other specs.
- OpenAPI for `POST /v1/invitations`: returns `201`; `400` for an invalid email; `403` for a role the caller may not grant; `409` when the address is already invited or a member. It accepts an optional `Idempotency-Key` header.
- The existing `e2e/invitations.spec.ts` has 2 tests that use `page.locator(".btn-primary")` and `page.waitForTimeout(2000)`.

## Plan

Journeys and states agreed with the user:

1. The owner invites a new address as Editor, and it appears in the pending list with a "Pending" badge.
2. An invalid email shows an inline error tied to the field, and no request is sent.
3. An address already invited (`409`) shows an announced error, and focus moves to the email field.
4. A member sees no Admin role option. If the mock forces a `403`, the error is shown.
5. A server error (`500`) shows a Retry control, and retrying succeeds once the mock recovers.
6. An empty list shows the empty state. While the list loads, the loading state is visible; the mock handler controls the delay, so the test never sleeps.
7. Double-clicking Send invite creates exactly one invitation.
8. Keyboard only: Tab to the field, type, press Enter to submit.
9. An axe scan of the dialog in its default and error states.

`typescript-test-engineer` owns the specs. The primary owns any product fix, using `frontend-react-engineering`.

## Specialist handoff

Handoff to `typescript-test-engineer`:

- Original goal: verify the invite journey before release; fix what is broken.
- In scope: `e2e/invitations.spec.ts`, mock handlers for invitations, component tests for `InviteForm`.
- Out of scope: product code (the primary owns it), other screens, CI configuration.
- Verified repository facts: the Perceive list above.
- Assumptions and unresolved decisions: the mock API matches the OpenAPI contract for invitations.
- Files or components affected: `src/features/invitations/**`, `mocks/handlers/invitations.ts`, `e2e/invitations.spec.ts`.
- Acceptance criteria: journeys 1–9 pass on both configured projects without fixed waits or CSS selectors.
- Risks and prohibited actions: never weaken an assertion to get a pass; no real API or real accounts; do not commit storage state or traces.
- Requested specialist output: failing journeys with trace evidence, spec changes, commands and results.
- Evidence gathered so far: the existing two tests pass on both projects.

Specialist response:

- Findings or changes:
  - Journey 7 failed on both projects. The trace's network log shows two `POST /v1/invitations` 40 ms apart, and the list shows two pending rows. This is a product defect: the button stays enabled while the request is pending, and no idempotency key is sent.
  - Journey 3 failed. The error text renders, but `getByRole("alert")` finds nothing and focus stays on the button. This is a product accessibility defect.
  - Journeys 1, 2, 4, 5, 6 and 8 passed.
  - The two existing tests, which already covered journeys 1 and 2, now use `getByRole("button", { name: "Send invite" })` and web-first assertions such as `await expect(row).toBeVisible()` in place of the fixed wait. What they assert is unchanged, and the diff notes this.
- Evidence and source locations: traces in `test-results/invitations-*/trace.zip`, kept locally.
- Tests performed and results: on both projects, 7 of 9 journeys passed; 3 and 7 failed as described.
- Open risks and confidence limitations: WebKit is not a configured project, so Safari behaviour is outside this run.
- Recommended next action: fix the product; leave the failing assertions as they are.

## Act

The product fixes, by the primary:

- `src/features/invitations/InviteForm.tsx`:
  - Disable submit while the mutation is pending and show "Sending…".
  - Generate one idempotency key per submission attempt with `crypto.randomUUID()`, and reuse it when that same attempt is retried.
  - On `400` or `409`, set `aria-invalid` and `aria-describedby` on the email input, render the message in a `role="alert"` region, and move focus to the input.
- `src/api/invitations.ts`: send the `Idempotency-Key` header.
- `mocks/handlers/invitations.ts`: honour the header as the OpenAPI contract describes (a replay returns the original `201`). The spec then exercises the contract rather than a mock shortcut. `api-contract-and-integration-engineering` motivates this: the client now depends on server idempotency, so the mock must model it.
- `src/features/invitations/InviteForm.test.tsx`: component tests for the disabled-while-pending state and focus-on-error.

Data exposure check (`frontend-react-engineering`):

- Fixture addresses use `@example.test`.
- The invitation token never appears in the UI, the URL or browser storage.
- Traces contain only the synthetic users' session and stay in the ignored `test-results/`.

## Verify

| Command | Result |
|---|---|
| `pnpm --filter admin-web typecheck` | 0 errors |
| `pnpm --filter admin-web test` | 187 passed (4 new) |
| `pnpm --filter admin-web exec playwright test e2e/invitations.spec.ts` (before fixes) | 4 failed (journeys 3 and 7 on each project); traces retained |
| Same command (after fixes) | 18 passed: 9 tests × 2 projects |
| `pnpm --filter admin-web exec playwright test e2e/invitations.spec.ts --repeat-each=5` | 90 passed, 0 flaky |
| axe scan inside journey 9 | 0 violations for the `wcag2a` and `wcag2aa` tags, default and error states |
| `git status --short` | only intended files; nothing from `playwright/.auth/` or `test-results/` |

## Completion report

- Recommendation: COMPLETE_VERIFIED
- Goal: verify the invitation journey before release and fix what is broken.
- Scope: `apps/admin-web` against its local preview server and mock API, on the two configured Playwright projects (Chromium and Firefox). Not claimed: the real API, a deployed environment, WebKit.

### Acceptance criteria

| Criterion | Status | Evidence or limitation |
|---|---|---|
| Journeys 1–8 pass on both configured projects | Verified | 18 of 18 after fixes; 90 of 90 with `--repeat-each=5` |
| Double submission creates one invitation | Verified | journey 7, plus the mock's request counter, now 1 |
| Errors are announced and focus moves to the field | Verified | journey 3 locates `getByRole("alert")` and asserts focus; component test |
| No fixed waits or CSS selectors in the spec | Verified | spec diff; `waitForTimeout` and class selectors removed |
| No automated accessibility violations in the dialog | Verified | axe scan, `wcag2a` and `wcag2aa` tags |
| No sensitive data committed or exposed | Verified | `git check-ignore`; `git status`; token absent from DOM, URL and storage assertions |

### Delivery evidence

- Files changed: `src/features/invitations/InviteForm.tsx`, `src/features/invitations/InviteForm.test.tsx`, `src/api/invitations.ts`, `mocks/handlers/invitations.ts`, `e2e/invitations.spec.ts`.
- Architecture decisions: client-generated idempotency keys per submission attempt, matching the existing API contract.
- Checks and results: as in Verify. The 4 failures before the fix were product defects, fixed in product code.
- Security review: done by the primary for data exposure only. No auth logic changed, so no independent security review was requested.
- Observability impact: none. The screen emits no new telemetry.
- Operational and cost impact: none; the change is client-side plus a header the API already accepts.
- Unverified items: none within scope. Outside it: WebKit, which is not configured in this repository (add it if Safari is supported); the real API's idempotency behaviour, which the contract documents and the mock models; screen-reader behaviour beyond automated axe checks and role assertions.
- Residual risks: automated accessibility checks find only a subset of issues; a manual pass with a screen reader is recommended before release.
- Rollback: revert the commit. There is no data or schema change.
