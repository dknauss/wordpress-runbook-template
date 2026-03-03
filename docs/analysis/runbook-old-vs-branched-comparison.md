# Runbook Comparison: Baseline vs Branched Phase Model

## Scope

This document compares two concrete versions of the WordPress operations runbook:

- **Baseline runbook ("old")**: `origin/main` at commit `153a035` (editorial corrections applied, before phased structural refactor)
- **Branched phase model ("new")**: `codex/runbook-model-p3-roles-and-validation` at commit `70a6fb7` (Phases 1-3 layered on top of the baseline)

Comparison target: `WP-Operations-Runbook.md` only.

## Change Size

From `origin/main...codex/runbook-model-p3-roles-and-validation`:

- Files changed: `1`
- Insertions: `415`
- Deletions: `270`
- Net delta: `+145` lines

## What Changed

1. **Procedure standardization (Phase 1)**
- Added a standard procedure block model in conventions.
- Refactored high-frequency operational paths to include explicit purpose/prereqs/commands/verification/rollback/escalation style elements.
- Key focus areas: Section 6, Section 8, and Section 10.2.

2. **Alert playbook model (Phase 2)**
- Converted major incident procedures to an alert-centric structure:
  - `Alert Meaning`
  - `Customer Impact`
  - `Diagnosis`
  - `Immediate Mitigation`
  - `Escalation`
  - `Recovery Validation`
- Applied to Section 10.2 (site down), 10.3 (security breach), and 10.5 (performance).

3. **Ownership + freshness controls (Phase 3)**
- Added incident role cards in Section 10.4.
- Added runbook freshness guardrails in Section 1.
- Added Appendix E matrix for `Owner`, `Last Tested`, `Review Cadence`, and `Last Drill Date` for critical procedures.

## Strengths and Weaknesses

## Old Runbook (Baseline)

### Strengths
- Simpler narrative flow with less process overhead.
- Faster initial reading for experienced operators who already know local systems.
- Lower documentation-maintenance burden in day-to-day operations.

### Weaknesses
- Inconsistent procedure structure across critical sections.
- Incident response sections were less alert-oriented and less explicit about customer impact and validation closure.
- Ownership and freshness metadata was not systematically embedded, increasing drift risk over time.
- Some operational commands/checkpoints were less copy/paste-safe or less explicit under pressure.

## New Runbook (Branched Phase Model)

### Strengths
- Stronger execution reliability under pressure via standardized procedure structure.
- Incident response is more operationally actionable due to explicit alert-playbook framing.
- Better accountability and lifecycle hygiene via role cards and Appendix E metadata controls.
- More explicit verification and escalation paths reduce ambiguous handoffs.

### Weaknesses
- Higher verbosity and cognitive overhead for quick scans.
- Higher maintenance cost (metadata freshness fields must be actively maintained).
- Mixed-mode risk if future edits apply the new model unevenly across untouched sections.
- Requires stronger editorial discipline to avoid process drift back to ad-hoc formats.

## Pros and Cons by Dimension

| Dimension | Old Runbook (Pros) | Old Runbook (Cons) | New Runbook (Pros) | New Runbook (Cons) |
|---|---|---|---|---|
| Speed to read | Compact and straightforward | Missing explicit closure checkpoints | More explicit decision scaffolding | More text to scan |
| Incident handling | Familiar ad-hoc flow | Weaker standardized response model | Alert-driven response consistency | Can feel heavyweight for small incidents |
| Operational safety | Lower friction for experts | More room for interpretation errors | Explicit validation/rollback/escalation pathways | Requires discipline to keep fields current |
| Governance | Minimal overhead | Weak ownership/freshness signals | Clear owner/test/review model | Ongoing upkeep workload |
| Auditability | Basic | Limited evidence trail in procedure metadata | Better traceability of readiness and drills | Metadata can become stale if not enforced |

## Practical Interpretation

- If your primary concern is **speed with minimal process overhead**, the old model is lighter.
- If your primary concern is **repeatable execution, incident quality, and operational governance**, the new model is materially stronger.
- For production teams with rotation/on-call turnover, the new model is generally the better long-term operating system.

## Recommendation

Adopt the **new branched phase model** as the target operating baseline, with two guardrails:

1. Keep procedure blocks concise to avoid documentation bloat.
2. Enforce Appendix E freshness updates as part of operational change management.

