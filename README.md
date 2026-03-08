# WordPress Operations Runbook Template

A comprehensive operations runbook template for WordPress sites running on standard LEMP (Nginx) or LAMP (Apache) stacks. This template provides the structure and procedures for creating a site-specific runbook tailored to your environment — fill in your configuration details, remove sections that don't apply, rename/replace [TEMPLATE/CUSTOMIZE] references, and you have a complete operational reference for your team. 

NB: The Version History table (§1.4) and Changelog (Appendix C) refer to the history of this document as a template. Reset/remove this information and add your own history of revisions to your operational document.

## Document Purpose

This is a template and model for creating an **operational reference** — it answers **"how do I do it?"** — for a specific WordPress installation.

Every procedure includes numbered steps, expected outcomes, rollback instructions, and copy-pasteable code. The target reader is a sysadmin or engineer responding to an incident, deploying an update, or setting up a new environment and needing exact commands and configurations to follow.

This document is **not** an audit checklist (use the [Security Benchmark](https://github.com/dknauss/wp-security-benchmark) for that), **not** an architectural guide (use the [Hardening Guide](https://github.com/dknauss/wp-security-hardening-guide)), and **not** a writing reference (use the [Style Guide](https://github.com/dknauss/wp-security-style-guide)).

## Audience

This template is intended for system administrators, DevOps engineers, site reliability teams, and WordPress developers responsible for the uptime, security, and operational integrity of WordPress deployments. It assumes a self-hosted or VPS-based environment with server-level access, though much of the content applies to any WordPress installation.

The template is designed to be adapted for a single WordPress site or instance. Organizations managing multiple sites should create a separate runbook for each environment, since server configurations, credentials, escalation contacts, and recovery procedures differ across deployments.

## What's Included

The runbook template is provided in four formats:

| File | Format | Best for |
|------|--------|----------|
| `WP-Operations-Runbook.md` | Markdown | Git repositories, wikis, version-controlled documentation |
| `WP-Operations-Runbook.docx` | Microsoft Word | Corporate intranets, SharePoint, collaborative editing |
| `WP-Operations-Runbook.epub` | EPUB | eBook readers |
| `WP-Operations-Runbook.pdf` | PDF | Printing, read-only distribution, archival |

Build pipeline: `WP-Operations-Runbook.md` -> `WP-Operations-Runbook.docx` -> `WP-Operations-Runbook.pdf` and `WP-Operations-Runbook.epub`.

All three documents contain identical content organized into 11 sections plus appendices:

1. **Document Information** — ownership, audience, document conventions
2. **Site Overview** — site identity, credentials vault, team contacts
3. **Environment Reference** — LEMP/LAMP architecture, service paths, caching layers, SSL/TLS configuration
4. **Development Workflow** — version control, staging environments, staging-to-production synchronization
5. **Security Hardening** — firewall configuration, SSH access, WordPress application hardening, HTTP security headers, REST API restrictions
6. **Routine Maintenance** — update calendar, core/plugin/theme updates, database optimization, PHP upgrades, WP-Cron configuration, transactional email, log rotation, uptime monitoring
7. **Backup Procedures** — backup strategy, verification, restoration testing
8. **Deployment Procedures** — code deployment, database migration, rollback procedures
9. **Content Operations** — media management (including WebP), editorial workflow, permalinks, search configuration
10. **Incident Response** — severity classification, site-down triage, security breach response, escalation paths, post-incident review, performance troubleshooting
11. **Disaster Recovery** — RTO/RPO targets, full-site restore, database recovery, server migration

**Appendices:** File permissions reference, `wp-config.php` key settings, change log

An **Emergency Quick-Reference Card** at the front provides at-a-glance triage steps for common failure scenarios.

## How to Use This Template

1. **Choose your format.** Use the Markdown file for Git-based documentation workflows. Use the Word or Pages file for collaborative editing in corporate environments. Use the PDF as a printed reference or read-only handoff.

2. **Search for `[CUSTOMIZE]` placeholders.** Every site-specific value is marked with this tag. Replace each placeholder with your actual configuration: server addresses, domain names, file paths, backup schedules, escalation contacts, and credentials vault references.

3. **Remove sections that don't apply.** Running Nginx? Remove the Apache references. Not using Multisite? Delete that section from Appendix B. The template is deliberately comprehensive — it is easier to remove what you don't need than to discover a gap during an incident.

4. **Assign ownership and schedule reviews.** Designate a runbook owner responsible for keeping the document current. Update the Change Log (Appendix C) whenever the environment changes, and schedule quarterly reviews to ensure the runbook reflects the actual state of the site.

## Design Principles

This template follows industry runbook conventions from Atlassian, Google SRE, and PagerDuty:

- Every procedure includes **numbered steps**, **expected outcomes**, and **time estimates**
- Warnings and critical notes are called out visually so they are not overlooked under pressure
- Rollback steps accompany every change procedure
- Escalation paths are defined within incident response workflows
- The Emergency Quick-Reference Card provides immediate routing to the correct procedure

## Related: Ops Runbook (Lite) WordPress Plugin

For teams that want operational procedures and diagnostics accessible directly within the WordPress Dashboard, the [Ops Runbook (Lite)](https://wordpress.org/plugins/ops-runbook-lite/) plugin provides three features inside `wp-admin`:

- **Runbook entries** — a custom post type with structured fields for symptoms, quick checks, mitigation steps, escalation contacts, and rollback procedures.
- **Incident notes** — a custom post type for incident timeline documentation and post-incident review.
- **Diagnostics page** — a read-only status page (under Tools) showing WordPress and plugin update status, WP-Cron scheduled tasks, disk storage metrics, database size, and the tail of the debug log.

The plugin complements this template: use this document as the comprehensive operational reference, and the plugin for quick in-Dashboard access to key procedures and system status.

## Related Documents

This runbook is one of four complementary documents covering WordPress security from different angles:

| Document | Purpose |
|---|---|
| **[WordPress Security Benchmark](https://github.com/dknauss/wp-security-benchmark)** | Audit checklist — "what to verify." Prescriptive, auditable hardening controls for compliance verification. |
| **[WordPress Security Hardening Guide](https://github.com/dknauss/wp-security-hardening-guide)** | Advisory — "what to implement." Enterprise-focused security architecture and threat mitigation. |
| **[WordPress Security Style Guide](https://github.com/dknauss/wp-security-style-guide)** | Editorial — "how to write about it." Terminology, voice, and formatting conventions for security communication. |

## Contributors

- [Dan Knauss](https://dan.knauss.ca) — author, editor
- [Claude](https://claude.ai) (Anthropic) — review, revision, cross-document alignment
- [Gemini](https://gemini.google.com) (Google) — independent review and revision planning
- [GPT-5 Codex](https://openai.com) (OpenAI) — independent review and revision planning

## AI-Assisted Editorial Process

This document and the three related documents in this series are revised with the assistance of frontier LLMs. Multiple models independently review all four documents for factual errors, outdated guidance, and cross-document misalignments, with the WordPress Advanced Administration Handbook as primary authority. A human editor reviews, approves, or rejects every recommended change before it is applied. For the full methodology, see **[AI-Assisted Documentation Processes](https://github.com/dknauss/ai-assisted-docs)**.

## Contributing

This is a general-purpose template. If you find gaps, errors, or have procedures that would benefit the broader WordPress community, pull requests are welcome. Please keep contributions environment-agnostic — no hosting-provider-specific or proprietary-tool-specific content.

## License

This template is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). You may copy, redistribute, remix, transform, and build upon this material for any purpose, including commercial use, provided you give appropriate credit and distribute your contributions under the same license.
