<div align="center">

# Go Live.skill

<p align="center">
  <img src="assets/go-live-cover.png" alt="Go Live skill cover" />
</p>

> *Ship the change, then send the public link.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-blueviolet)](https://github.com/openai/codex)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

**Go Live is a Codex skill for mobile-first Codex workflows.**

When you use Codex from the ChatGPT mobile app, localhost is not a useful preview. Go Live asks Codex to deploy and verify the app, website, or frontend change, then send back a public URL you can open on your phone.

English | [中文](README.md)

</div>

---

## Install

If you use Codex from the CLI:

```bash
npx skills add Sac-Y/go-live
```

If you use Codex App or Codex in the ChatGPT mobile app, tell Codex:

```text
Please install this skill:
https://github.com/Sac-Y/go-live
```

---

## Usage

Go Live is not tied to a specific deployment provider. Codex should first inspect the project and reuse the existing deployment path. If Vercel, Cloudflare, GitHub, or another plugin capability is needed, Codex can ask for installation or authorization during the task.

After installing, say things like:

```text
"Help me preview this page on my phone. Send me a link after you finish."
"I want to edit this site while checking it on mobile. Deploy it after each change."
"After this frontend change, send me a public preview link."
```

Its workflow is simple:

1. Make the requested code, content, or design change.
2. Run the fastest meaningful project check, such as build, lint, typecheck, or smoke test.
3. Reuse the project's existing deployment path, such as Vercel, Netlify, Cloudflare, Firebase, GitHub Pages, or CI/CD.
4. Open the public URL and verify that the page loads with the latest change.
5. Reply with the public URL, what changed, and the verification result.

Notes:

- Do not leave only a localhost URL unless the user explicitly asks for local-only preview.
- If the project already has a deployment provider, keep using it instead of creating a new one.
- If deployment needs login, project linking, environment variables, or commit/push, Codex should explain the blocker and the next step.
- Do not claim deployment succeeded before checking the public URL.

---

## License

MIT
