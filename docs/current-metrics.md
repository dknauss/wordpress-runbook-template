# Current Metrics (Canonical)

This file is the single source of truth for architectural counts in the WordPress Operations Runbook. Check this file before writing any count in prose, and update it when adding or removing procedures, commands, or structural elements.

Last verified: 2026-10-07

## Architectural Facts

| Fact | Value | Verification command | Last changed |
|---|---:|---|---|
| Document lines | 3,629 | `wc -l WP-Operations-Runbook.md` | 2026-10-07 |
| Major sections | 11 | `grep -cE '^## Section' WP-Operations-Runbook.md` | v3.0 |
| Appendices | 5 | `grep -cE '^## Appendix' WP-Operations-Runbook.md` | v3.0 |
| WP-CLI commands (total) | 148 | `grep -cE '^\s*wp ' WP-Operations-Runbook.md` | 2026-10-07 |
| Destructive WP-CLI commands | 44 | `grep -cE '^\s*wp (search-replace|db import|db reset|db query|post delete|comment delete|user delete|plugin delete|plugin deactivate|option update|option delete|rewrite flush|transient delete|cache flush|eval|eval-file)' WP-Operations-Runbook.md` | 2026-10-07 |
| Commented-out WP-CLI commands | 16 | `grep -cE '^\s*# wp ' WP-Operations-Runbook.md` | 2026-10-07 |
| Inline WARNING comments (`# WARNING:`) | 34 | `grep -c '# WARNING:' WP-Operations-Runbook.md` | 2026-10-07 |
| Blockquote WARNING callouts | 22 | `grep -c '> \*\*WARNING:\*\*' WP-Operations-Runbook.md` | 2026-10-07 |
| `[CUSTOMIZE: ...]` placeholders | 217 | `grep -c '\[CUSTOMIZE:' WP-Operations-Runbook.md` | 2026-10-07 |
| Plugin-dependent annotations | 8 | `grep -c '# Plugin-dependent' WP-Operations-Runbook.md` | 2026-10-07 |
| Code fences (total) | 180 | `grep -c '^\`\`\`' WP-Operations-Runbook.md` | 2026-10-07 |
| Opening fences (with language tag) | 85 | `grep -cE '^\`\`\`[a-z]' WP-Operations-Runbook.md` | 2026-10-07 |
| Bare closing fences | 95 | `grep -cE '^\`\`\`$' WP-Operations-Runbook.md` | 2026-10-07 |
| Output formats | 4 | Markdown, DOCX, EPUB, PDF | v3.0 |

## Safety Ratios

These derived metrics help evaluate whether the document maintains adequate safety coverage.

| Ratio | Current | Target | Notes |
|---|---|---|---|
| Inline warnings / destructive commands | 34 / 44 (77%) | 100% of high-risk commands | Not all destructive commands need inline warnings (e.g., `wp cache flush` in a "Clear Caches" step is low-risk). Focus on commands that destroy unrecoverable data. |
| Opening fences / closing fences | 85 / 95 | Equal or explainable | Difference of 10 is expected: some code blocks open with bare ``` (no language tag). A mismatch that can't be explained indicates a corrupted fence. |

## Verification Procedure

Run all verification commands after any structural edit to the runbook:

```bash
cd "$(git rev-parse --show-toplevel)"

echo "=== Document size ==="
wc -l WP-Operations-Runbook.md

echo "=== Structure ==="
echo "Sections: $(grep -cE '^## Section' WP-Operations-Runbook.md)"
echo "Appendices: $(grep -cE '^## Appendix' WP-Operations-Runbook.md)"

echo "=== Commands ==="
echo "WP-CLI total: $(grep -cE '^\s*wp ' WP-Operations-Runbook.md)"
echo "Destructive: $(grep -cE '^\s*wp (search-replace|db import|db reset|db query|post delete|comment delete|user delete|plugin delete|plugin deactivate|option update|option delete|rewrite flush|transient delete|cache flush|eval|eval-file)' WP-Operations-Runbook.md)"
echo "Commented-out: $(grep -cE '^\s*# wp ' WP-Operations-Runbook.md)"

echo "=== Safety ==="
echo "Inline WARNINGs: $(grep -c '# WARNING:' WP-Operations-Runbook.md)"
echo "Blockquote WARNINGs: $(grep -c '> \*\*WARNING:\*\*' WP-Operations-Runbook.md)"
echo "Plugin-dependent: $(grep -c '# Plugin-dependent' WP-Operations-Runbook.md)"
echo "CUSTOMIZE placeholders: $(grep -c '\[CUSTOMIZE:' WP-Operations-Runbook.md)"

echo "=== Code fences ==="
echo "Total: $(grep -c '^```' WP-Operations-Runbook.md)"
echo "Opening (with tag): $(grep -cE '^```[a-z]' WP-Operations-Runbook.md)"
echo "Bare closing: $(grep -cE '^```$' WP-Operations-Runbook.md)"
```

## Update Procedure

1. After any edit to `WP-Operations-Runbook.md`, run the verification script above.
2. Compare results to this table. Update any changed values.
3. If a destructive command was added without a WARNING, add one before committing.
4. If opening/closing fence counts diverge unexpectedly, find and fix the broken fence.
5. Update `CHANGELOG.md` with the change.
