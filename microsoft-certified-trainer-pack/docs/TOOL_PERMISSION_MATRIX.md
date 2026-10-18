# Tool Permission Matrix

| Capability | Typical use | Default evidence | Gate |
|---|---|---|---|
| Read/search/web | Inspect courseware and current Microsoft sources | Static/source evidence | No mutation |
| Edit/execute | Author or validate local course assets | Local result | Review changed files |
| PPTX/PDF/Office inspection | Extract structure, notes, links, accessibility cues | Static inspection | No external publish |
| Browser/Playwright | Inspect a documented UI or rehearse a demo | Local rehearsal | Do not enter real learner data |
| Git/GitHub | Version course assets and run checks | Local or API evidence | Repository write approval |
| Azure/Graph/Microsoft APIs | Verify or prepare lab dependencies | API/static result | Tenant, identity, cost, and publish approval |
| Copilot Studio | Design, preview, test, evaluate | Preview/test evidence | Publish and connector changes require approval |
| External communication | Send course or learner updates | Draft only | Explicit send approval |

