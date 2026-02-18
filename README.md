# WordPress Runbook Template

A comprehensive, ready-to-customize operations runbook for WordPress sites running on standard LEMP (Nginx) or LAMP (Apache) stacks. (.md, .docx, .pages, .pdf)

## Who is this for?

This template is designed for anyone responsible for keeping a WordPress site running reliably — whether that's a solo freelancer managing client sites, a small agency ops team, or an in-house sysadmin at an organization that runs WordPress. It assumes a self-hosted or VPS-based environment (not managed/shared hosting where you have no server access), though much of the content applies to any WordPress installation.

If you've ever been paged at 2 AM and wished you had a step-by-step guide for "the site is down, now what?" — this is that guide, plus everything else you need documented before that call comes in.

## What's included

| File | Format | Best for |
|------|--------|----------|
| `WP-Operations-Runbook.docx` | Microsoft Word | Editing, internal wikis, corporate environments |
| `WP-Operations-Runbook.md` | Markdown | GitHub/GitLab wikis, static sites, version control |
| `WP-Operations-Runbook.pdf` | PDF | Printing, read-only distribution, archival |

All three contain identical content organized into 11 sections plus appendices:

1. **Document Information** — ownership, audience, conventions
2. **Site Overview** — identity, credentials vault, team contacts
3. **Environment Reference** — LEMP/LAMP architecture, service paths, caching layers, SSL/TLS
4. **Development Workflow** — version control, staging environments, staging-to-production sync
5. **Security Hardening** — firewall, SSH, WordPress-level hardening, HTTP headers, REST API lockdown
6. **Routine Maintenance** — update calendar, core/plugin/theme updates, database optimization, PHP upgrades, WP-Cron, transactional email, log rotation, monitoring
7. **Backup Procedures** — strategy, verification, testing
8. **Deployment Procedures** — code deployment, database migration, rollback
9. **Content Operations** — media management (with WebP guidance), editorial workflow, permalinks, search
10. **Incident Response** — severity classification, site-down triage, breach response, escalation, post-mortems, performance troubleshooting
11. **Disaster Recovery** — RTO/RPO targets, full restore, database recovery, server migration

**Appendices:** File permissions reference, wp-config.php key settings, change log

An **Emergency Quick-Reference Card** at the front provides at-a-glance triage for the most common failure scenarios.

## How to use it

1. **Pick your format.** Use the `.md` if you want to keep it in a Git repo alongside your code. Use the `.docx` if your team prefers Word or a wiki. Use the `.pdf` for a printed binder or read-only handoff.

2. **Search for `[CUSTOMIZE]`.** Every site-specific field is marked with this placeholder. Go through each one and fill in your actual values — server IPs, domain names, backup schedules, escalation contacts, etc.

3. **Delete what doesn't apply.** Running Nginx? Remove the Apache references. Not using Multisite? Delete that section from Appendix B. The template is deliberately comprehensive so you can trim it down rather than guess what's missing.

4. **Keep it alive.** A runbook is only useful if it's current. Update the Change Log (Appendix C) whenever you change your environment, and schedule a quarterly review to catch drift.

## Design principles

This template follows industry runbook models from Atlassian, Google SRE, and PagerDuty:

- Every procedure includes **numbered steps**, **expected outcomes** (so you know it worked), and **time estimates**
- Warnings and notes are called out visually so they aren't missed under pressure
- Rollback steps are provided for every change procedure
- Escalation paths are built into incident response
- The Emergency Quick-Reference Card gets you to the right procedure in seconds, not minutes

## Related: Ops Runbook (Lite) WordPress Plugin

If you want operational runbook content accessible directly inside wp-admin rather than in an external document, take a look at [Ops Runbook (Lite)](https://wordpress.org/plugins/ops-runbook-lite/) — a WordPress plugin that provides admin-only ops runbooks and a one-click diagnostics panel within the WordPress dashboard. It's a good complement to this template: use this document for your full operational reference, and the plugin for quick in-dashboard access to diagnostics and key procedures without leaving wp-admin.

## Contributing

This is a general-purpose template. If you find gaps, errors, or have procedures that would benefit others, pull requests are welcome. Please keep contributions environment-agnostic (no hosting-provider-specific or proprietary-tool-specific content).

## License

This template is provided as-is for use by WordPress site operators. Feel free to adapt it for your organization.
