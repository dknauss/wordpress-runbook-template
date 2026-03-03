# Roadmap

## Item: Operational Runbook Model Upgrade

- Status: Proposed
- Priority: High
- Type: Documentation architecture and operations reliability
- Scope: `WP-Operations-Runbook.md` only (keep Benchmark/Hardening/Style separation intact)
- Target window: Q2 2026

### Problem
The runbook is comprehensive, but operational procedures are not yet standardized into a machine-friendly and alert-friendly format. This increases copy/paste risk, slows incident execution, and makes ongoing validation harder.

### Goals
1. Standardize procedure structure for execution under pressure.
2. Convert key incident content to alert playbook format.
3. Add ownership and freshness metadata for continuous reliability.
4. Preserve strict operational focus (no architecture/audit drift).

### Non-Goals
1. Rewriting companion documents (Benchmark, Hardening Guide, Style Guide).
2. Large content expansion outside operations use cases.
3. Introducing provider-specific tooling dependencies.

### Success Criteria
1. Every high-frequency operational procedure includes: prerequisites, exact commands, expected output, rollback, verification.
2. Incident section includes alert-playbook blocks (`meaning`, `impact`, `diagnosis`, `mitigation`) for top scenarios.
3. Runbook procedures include owner + last-tested metadata.
4. Zero invalid or ambiguous command examples in core maintenance/incident paths.

### Milestones
1. Phase 1: Procedure Template Standardization.
2. Phase 2: Alert Playbook Conversion for Incident Workflows.
3. Phase 3: Incident Role Cards + Validation Cadence Metadata.

### Risks and Mitigations
1. Risk: Over-formatting reduces readability.
   Mitigation: Use concise, repeatable blocks and preserve current section hierarchy.
2. Risk: Scope creep into non-operational guidance.
   Mitigation: Reject changes that duplicate benchmark/hardening rationale.
3. Risk: Command drift over time.
   Mitigation: Add explicit validation cadence and owner accountability.
