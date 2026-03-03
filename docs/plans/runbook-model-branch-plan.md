# WP Runbook Branch and PR Plan

## Objective
Implement the runbook model upgrade in small, reviewable PRs while preserving the runbook's operational-only purpose.

## Branch Strategy
- Base branch: `main`
- Planning branch: `codex/runbook-model-roadmap-plan`
- Integration branch: `codex/structured-runbook-v3` (cherry-picked from Codex phases onto corrected main)
- Original Codex execution branches (for reference):
  1. `codex/runbook-model-p1-procedure-template`
  2. `codex/runbook-model-p2-alert-playbooks`
  3. `codex/runbook-model-p3-roles-and-validation`

## Implementation Note

The original Codex branches were created before Round 2 editorial corrections (19 findings) were applied to main. Rather than rebasing, the structural improvements were cherry-picked onto the corrected main to avoid regression risk. See `REVISION-LOG.md` in the [ai-assisted-docs](https://github.com/dknauss/ai-assisted-docs) repo for the full list of corrections.

## PR Breakdown

### PR 1: Procedure Template Standardization
- Scope:
  1. Define a reusable runbook procedure block:
     - `Purpose`
     - `Prerequisites`
     - `Commands`
     - `Expected Output`
     - `Rollback`
     - `Verification`
     - `Escalate If`
  2. Apply this format to highest-frequency operations:
     - Section 6.2, 6.3, 6.6 (Routine Maintenance)
     - Section 8.1, 8.2, 8.3 (Deployment Procedures)
- Exit criteria:
  1. No procedural step without verification/rollback guidance.
  2. Commands are copy/paste-safe and reviewed for syntax validity.

### PR 2: Alert Playbook Conversion
- Scope:
  1. Add alert playbook blocks for recurring incidents in Section 10:
     - 10.2 Site down / 500
     - 10.3 Security breach response
     - 10.5 Performance degradation
  2. Standard block shape:
     - `Alert Meaning`
     - `Customer Impact`
     - `Diagnosis`
     - `Immediate Mitigation`
     - `Escalation`
     - `Recovery Validation`
- Exit criteria:
  1. On-call reader can route from symptom to first action in under 60 seconds.

### PR 3: Roles and Validation Cadence
- Scope:
  1. Add explicit incident role cards (Incident Commander, Technical Lead, Communications Lead, Scribe).
  2. Add lifecycle metadata (Owner, Last Tested, Review Cadence, Last Drill Date).
  3. Add Appendix E: Procedure Ownership and Validation Matrix.
  4. Add §1.5 Freshness Guardrails.
- Exit criteria:
  1. Every critical incident workflow has role ownership and freshness metadata.

## Review Model
1. Keep comments anchored to operational usability under incident pressure.
2. Require at least one reviewer to execute a dry-run for changed procedures.
3. Reject prose-only changes that do not improve execution reliability.

## Definition of Done (Program-Level)
1. Procedures are consistent and executable.
2. Incident pathways are alert-oriented and role-driven.
3. Freshness metadata is present for critical runbook paths.
4. Document remains operations-focused and complementary to companion security docs.
