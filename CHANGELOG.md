# Changelog

All notable changes to the WordPress Operations Runbook template.

## Unreleased

### Fixed
- Corrected findings from the 2026-10-07 documentation review and verification round. Recorded in `ai-assisted-docs/reviews/rounds/2026-10-07/`.
- §5.4: replaced the REST users-route example, which raised a fatal error on PHP 8 and replaced per-operation authorization on write handlers, with a tested snippet that requires authentication for reads and preserves core's permission checks.
- §11.2: full restore now keeps MySQL running, verifies configuration before the import, restores the separate uploads archive, and sets a `wp-config.php` mode the PHP-FPM pool user can read.
- §5.1: UFW rules are staged before the firewall is enabled; added an SSH port-change procedure, `KbdInteractiveAuthentication no`, and effective-configuration checks.
- §10.3: incident containment is now a verified web-server or edge block; `wp maintenance-mode activate` is labeled as not containment, and the Nginx `allow`/`deny` order is corrected.
- §5.5: separated 2FA enrollment, enforcement, and verification; the `two-factor` plugin has no built-in role enforcement.
- §5.4: `xmlrpc_enabled` is described as a partial measure; added a POST-based verification.
- §9.1: corrected the offload plugin slug and configuration method; WebP delivery now falls back to the original image.
- §10.5 autoload queries match the WordPress 6.6+ autoload values; PHP memory triage checks the PHP-FPM runtime.
- Appendix A: `wp-config.php` ownership and mode follow the PHP-FPM pool user (440 for the reference stack).
- §5.5: added a tested must-use plugin that enforces 2FA enrollment for privileged roles.
- §7.2: the backup script runs as the site user (WP-CLI refuses to run as root), verifies archives with `gzip -t`, and writes a SHA-256 manifest that §11.2 checks before restoring.
- §5.6: AIDE commands corrected for Debian and Ubuntu (`--config` is required; the initial database move failed on a fresh install).
- §9.1 offload settings keys verified against the plugin source; PHP upgrade step names the pool settings to carry over.
- CSP example notes the `worker-src` requirement of WordPress 7.1 client-side media processing.

### Changed
- Regenerated the PDF, DOCX, and EPUB files from the corrected Markdown and refreshed the PDF visual baselines, which had not been updated since March 2026.
- §3.2: split the service reference table into two narrower tables so it fits the PDF page. Generated artifacts have not been rebuilt.
- `CONTRIBUTING.md` describes the current manual build and release flow instead of an automatic publish on merge.
- `CLAUDE.md` uses portable command names.
- Updated `docs/current-metrics.md` for the above.

## 3.1.1 — 2026-06-17

### Added
- Added release-metadata validation so frontmatter version/date and the latest changelog release heading stay aligned, with optional tag/date enforcement during release publication.
- Added a `Series review` issue form so quarterly and pre-release cross-document alignment checks can be tracked explicitly.
- Added a repo-local generated-artifact smoke validator and a dedicated `Validate Artifacts` workflow for PDF, EPUB, and DOCX outputs.
- Added a Playwright-based PDF visual smoke test and dedicated workflow with committed baselines for critical page regions.
- Added a cross-format parity check so a small set of canonical phrases must remain present in the Markdown source and generated PDF, EPUB, and DOCX outputs.
- Added Learn WordPress's [Writing in the WordPress voice](https://learn.wordpress.org/course/writing-in-the-wordpress-voice/) as the recommended WordPress-specific voice and accessibility reference when runbook material is adapted into user-facing or cross-team communications.

### Changed
- Moved full PDF/DOCX/EPUB publication to the tag-driven release workflow and converted `generate-docs.yml` into a manual preview/build workflow instead of an automatic `main`-push publisher.
- Made the generated-artifact validator read the expected version string from the Markdown frontmatter instead of hardcoding `Version 3.1`, preventing future publish-flow failures after routine version bumps.
- Updated Section 1.4 of the canonical runbook so the in-document version history matches the actual template release history (`3.1`, `3.0.1`, `3.0`, `2.0`) instead of stale placeholder entries.
- Separated Playwright PDF visual validation from the artifact publish path so `generate-docs.yml` can publish after artifact checks while the dedicated visual workflow handles layout regression checks on workflow, packaging, and Pandoc changes.
- Aligned more of the operational procedures with the current runbook-skill safety rules by normalizing the cache-plugin annotation string, correcting the remaining singular `--field` WP-CLI examples to explicit `--fields=... --format=csv` pipelines, and adding approval/warning markers around additional side-effect commands (`wp db query` migrations, cache flushes, imports, option updates, transient deletion, and `wp eval-file` test mail).
- Corrected the example WordPress version placeholder to reflect the WordPress 7.0 release state.
- Refactored the document-generation pipeline into explicit build, validate, and publish jobs so generated artifacts are validated before the bot commit step runs.
- Updated GitHub Action pins in the PDF visual validation workflow to Node 24-capable major versions to avoid runner deprecation warnings.
- Set a short PDF running header title so the customizable subtitle no longer appears in page headers.
- Hardened GitHub release automation and metrics validation by pinning action references to immutable commits.
- Documented the maintainer edit, verification, artifact-generation, release, and cross-document review workflow for this repository and its companion document series.

## 3.1.0 — 2026-03-21

### Changed
- Standardized license metadata on the canonical Creative Commons legal text and normalized in-repo references to `CC-BY-SA-4.0`.
- Added explicit repository health files (`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`, `.gitattributes`) and linked them from the README so the repo no longer relies on inherited defaults for contributor guidance.
- Added a shared `Project Health` section in the README and aligned contributor and AI-assisted editorial copy with the rest of the security-document series.
- Bumped the canonical runbook frontmatter date/version to `March 21, 2026` / `3.1` for the synchronized minor release.

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
