# Current Metrics (Canonical)

This file is the single source of truth for architectural counts in the WordPress Operations Runbook. Check this file before writing any count in prose, and update it when adding or removing procedures, commands, or structural elements.

Last verified: 2026-03-15

## Architectural Facts

| Fact | Value | Verification command | Last changed |
|---|---:|---|---|
| Document lines | 3,273 | `wc -l WP-Operations-Runbook.md` | 2026-03-15 |
| Major sections | 11 | `grep -cE '^## Section' WP-Operations-Runbook.md` | v3.0 |
| Appendices | 5 | `grep -cE '^## Appendix' WP-Operations-Runbook.md` | v3.0 |
| WP-CLI commands (total) | 152 | `grep -cE '^\s*wp ' WP-Operations-Runbook.md` | 2026-03-15 |
| Destructive WP-CLI commands | 49 | `grep -cE '^\s*wp (search-replace|db import|db reset|db query|post delete|comment delete|user delete|plugin delete|plugin deactivate|option update|option delete|rewrite flush|transient delete|cache flush|eval|eval-file)' WP-Operations-Runbook.md` | 2026-03-15 |
| Commented-out WP-CLI commands | 13 | `grep -cE '^\s*# wp ' WP-Operations-Runbook.md` | v3.0-post |
| Inline WARNING comments (`# WARNING:`) | 16 | `grep -c '# WARNING:' WP-Operations-Runbook.md` | v3.0-post |
| Blockquote WARNING callouts | 15 | `grep -c '> \*\*WARNING:\*\*' WP-Operations-Runbook.md` | v3.0 |
| `[CUSTOMIZE: ...]` placeholders | 203 | `grep -c '\[CUSTOMIZE:' WP-Operations-Runbook.md` | 2026-03-15 |
| Plugin-dependent annotations | 6 | `grep -c '# Plugin-dependent' WP-Operations-Runbook.md` | 2026-03-15 |
| Code fences (total) | 166 | `grep -c '^\`\`\`' WP-Operations-Runbook.md` | 2026-03-15 |
| Opening fences (with language tag) | 78 | `grep -cE '^\`\`\`[a-z]' WP-Operations-Runbook.md` | 2026-03-15 |
| Bare closing fences | 88 | `grep -cE '^\`\`\`$' WP-Operations-Runbook.md` | 2026-03-15 |
| Output formats | 4 | Markdown, DOCX, EPUB, PDF | v3.0 |

## Safety Ratios

These derived metrics help evaluate whether the document maintains adequate safety coverage.

| Ratio | Current | Target | Notes |
|---|---|---|---|
| Inline warnings / destructive commands | 16 / 49 (33%) | 100% of high-risk commands | Not all destructive commands need inline warnings (e.g., `wp cache flush` in a "Clear Caches" step is low-risk). Focus on commands that destroy unrecoverable data. |
| Opening fences / closing fences | 78 / 88 | Equal or explainable | Difference of 10 is expected: some code blocks open with bare ``` (no language tag). A mismatch that can't be explained indicates a corrupted fence. |

## Verification Procedure

Run all verification commands after any structural edit to the runbook:

```bash
cd /Users/danknauss/Documents/GitHub/wordpress-runbook-template

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
