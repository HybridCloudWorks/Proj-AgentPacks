---
description: "Design or repair a cost allocation, showback or chargeback model"
argument-hint: "organization structure, current tagging state, target (showback or chargeback)"
agent: finops-professional-practitioner
---

# Design an allocation model

## Inputs

The organizational structure to express, the current hierarchy and taxonomy, at least one month of tagged billing data, the shared services in use and Finance's requirements for charges.

## Workflow

Apply cost-allocation-and-chargeback. Map the hierarchy first, define a short taxonomy, measure coverage on usage EffectiveCost, draft enforcement at creation with an exception path, define each shared-cost pool and key, handle Kubernetes and idle capacity explicitly, and check the chargeback entry criteria before proposing any charge. Ask finops-evidence-reviewer to check that allocations sum to the total before publication.

## Expected output

A one-page methodology, the taxonomy and enforcement drafts, a coverage report with its query, a showback draft with the unallocated line visible, the maturity next step with its entry criteria, and the completion report from the `finops-professional-practitioner-contract` instruction. Applying policies, retagging and publishing charges are Level 2.
