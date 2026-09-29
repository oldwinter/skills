---
name: browser
description: This skill should be used for browser automation tasks using Chrome DevTools Protocol (CDP). Triggers when users need to launch Chrome with remote debugging, navigate pages, execute JavaScript in browser context, capture screenshots, or interactively select DOM elements. No MCP server required.
---

# Browser Automation

Minimal Chrome DevTools Protocol (CDP) helpers for browser automation without MCP server setup.

## Setup

Run the setup from the skill directory before first use:

```bash
cd /path/to/browser
npm install --prefix browser
```

## Scripts

All scripts connect to Chrome on `localhost:9222`.

### start.cjs - Launch Chrome

```bash
node scripts/start.cjs              # Fresh profile
node scripts/start.cjs --profile    # Use persistent profile (keeps cookies/auth)
```

### nav.cjs - Navigate

```bash
node scripts/nav.cjs https://example.com        # Navigate current tab
node scripts/nav.cjs https://example.com --new  # Open in new tab
```

### eval.cjs - Execute JavaScript

```bash
node scripts/eval.cjs 'document.title'
node scripts/eval.cjs '(() => { const x = 1; return x + 1; })()'
```

Use single expressions or IIFE for multiple statements.

### screenshot.cjs - Capture Screenshot

```bash
node scripts/screenshot.cjs
```

Returns `{ path, filename }` of saved PNG in temp directory.

### pick.cjs - Visual Element Picker

```bash
node scripts/pick.cjs "Click the submit button"
```

Returns element metadata: tag, id, classes, text, href, selector, rect.

## Workflow

1. Launch Chrome: `node scripts/start.cjs --profile` for authenticated sessions
2. Navigate: `node scripts/nav.cjs <url>`
3. Inspect: `node scripts/eval.cjs 'document.querySelector(...)'`
4. Capture: `node scripts/screenshot.cjs` or `node scripts/pick.cjs`
5. Return gathered data

## Key Points

- All operations run locally - credentials never leave the machine
- Use `--profile` flag to preserve cookies and auth tokens
- Scripts return structured JSON for agent consumption
