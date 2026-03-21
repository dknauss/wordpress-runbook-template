# Changelog

All notable changes to the WordPress Operations Runbook template.

## Unreleased

## 3.0.1 — 2026-03-15

### Changed
- Reworked backup, restore, rollback, and deployment procedures to remove unsafe raw-datadir deletion, normalize backup paths and artifact formats, require known-good filesystem artifacts for rollback, and keep live plugin/theme updates out of deployment workflows.
- Expanded authentication guidance to cover privileged roles beyond single-site administrators, added a dedicated action-gated reauthentication / sudo-mode procedure, and clarified break-glass and application-password handling during recovery and incident response.
- Updated WordPress and PHP environment placeholders for the WordPress 7.0 release cycle, kept the PHP baseline at `8.3+` with `8.4` staging validation guidance, clarified self-managed versus managed-hosting assumptions, and aligned glossary/operator terminology around `Dashboard`, `WP-Cron`, `Multisite`, and related security terms.
- Corrected WP-CLI post-status and term-deletion examples, removed invalid or misleading SMTP and `wp-config.php` examples, fixed PHP package guidance, normalized Dashboard casing, and replaced hard-coded table-prefix examples where practical.
- Added centered page numbering to `.github/pandoc/reference.docx` so DOCX-derived PDF output includes footer page numbers through the shared generation pipeline.
- Replaced the repo-local document-generation workflow with a caller to the shared reusable workflow in `ai-assisted-docs`, keeping the primary markdown source and generated artifact names unchanged.

### Fixed
- Added missing inline `# WARNING:` comments before 10 destructive WP-CLI commands across sections 4, 6, 8, 9, 10, and 11. Commands fixed: `wp db import`, `wp search-replace` (4 instances), `wp post delete --force`, `wp comment delete --force`, `wp rewrite flush`, `wp plugin delete`, `wp user delete`, `wp db reset --yes`, `wp option update home/siteurl` (2 instances). Caught by BDD cycle test against `wordpress-runbook-ops` scenarios in [ai-assisted-docs](https://github.com/dknauss/ai-assisted-docs/blob/main/scenarios/test-runs/2026-03-11-runbook-ops-domain-migration.md).

### Added
- `CHANGELOG.md` — this file.
- `docs/current-metrics.md` — architectural fact counts with verification commands.

## 3.0 — 2026-03-08

- Full document revision: restructured all 11 sections, standardized procedure schema (Metadata, Purpose, Prerequisites, Commands, Expected Output, Rollback, Verification, Escalate If), added lifecycle metadata tracking in Appendix E.
- Fixed all WP-CLI command validity issues identified in Phase 1 audit (nonexistent flags, incorrect subcommands).
- Added Emergency Quick-Reference Card.
- Added incident response lifecycle tracking (Appendix E).
- Added `[CUSTOMIZE: ...]` placeholder format throughout.
- Added plugin-dependent command annotation pattern.
- Generated DOCX, EPUB, and PDF outputs from Markdown source.

## 2.0 — 2026-03-03

- Initial public release with 11 sections and 5 appendices.
