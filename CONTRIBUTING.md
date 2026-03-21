# Contributing

Thanks for helping improve the WordPress Operations Runbook template.

## Scope

Contributions are welcome for:

- factual corrections
- outdated WordPress or operations guidance
- safer command examples and warning coverage
- broken links or repository automation issues

This repository is an environment-agnostic operations template. It is not the
place for site-specific secrets, internal escalation contacts, or
hosting-provider-specific procedures unless they are clearly marked as optional
and broadly reusable.

## Before You Start

Read these files first:

- `README.md`
- `WP-Operations-Runbook.md`
- `docs/current-metrics.md`
- `SECURITY.md`

Related repositories in this document series may also need aligned updates:

- `wp-security-benchmark`
- `wp-security-hardening-guide`
- `wp-security-style-guide`

## Reporting Issues

- Use the GitHub issue templates for inaccurate procedures, broken examples, or
  improvement requests.
- Do not use public issues for security-sensitive reports. Follow
  `SECURITY.md` instead.

When filing a documentation bug, include the affected procedure or appendix,
the source used to verify the issue, and whether companion repos may also need
updates.

## Editing Rules

- Treat `WP-Operations-Runbook.md` as the canonical source.
- Keep generated artifacts aligned with the canonical Markdown source, but do
  not hand-edit binary artifacts unless the change specifically targets the
  generation pipeline or template files.
- Keep the template environment-agnostic. Replace site-specific examples with
  placeholders or clearly marked alternatives.
- Verify WordPress-specific commands and terminology against primary sources
  such as `developer.wordpress.org`, WP-CLI documentation, or WordPress core
  documentation.
- If a destructive command is added or made more prominent, review nearby
  warnings and rollback guidance.
- Update `CHANGELOG.md` for user-visible documentation or workflow changes.

## Metrics Verification

If your change affects sections, command counts, warnings, placeholders, or
other structural counts, update `docs/current-metrics.md` and run:

```bash
bash .github/scripts/verify-metrics.sh docs/current-metrics.md
```

The metrics file is the canonical source of truth for the structural counts
used in this repository.

## Generated Documents

This repository tracks generated `.docx`, `.epub`, and `.pdf` artifacts.
Regenerate them through the documented GitHub Actions workflow or an equivalent
local Pandoc toolchain when required by the change.

If you cannot regenerate artifacts locally, note that in the pull request
instead of committing guessed outputs.

## Pull Requests

Pull requests should:

- describe what changed and why
- mention any source or command verification performed
- note whether metrics, changelog entries, or generated artifacts changed
- call out any cross-document follow-up needed in the benchmark, hardening
  guide, or style guide repos

Keep changes focused. Separate template safety fixes from unrelated repository
or workflow changes when practical.
