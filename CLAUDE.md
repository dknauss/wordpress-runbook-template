# Claude guidance for this repository

<!-- claude-playwright-handoff -->
## Browser and Playwright handoff

If a task in this repository requires browser automation, Playwright testing, screenshots, page interaction, or browser-only inspection:

- Say clearly that a fresh browser-capable Claude session is required.
- Do not imply that Playwright or browser mode can be enabled from inside the current session.
- Tell the user to restart with `/Users/danknauss/bin/claude-playwright` or `/Users/danknauss/bin/claude-browser-handoff`.

Use this only when browser tooling is actually needed, not when it is merely convenient.
