<div align="center">

# Go Live.skill

<p align="center">
  <img src="assets/go-live-cover.png" alt="Go Live skill cover" />
</p>

**Localhost 到不了的地方，Go Live 帮你送达**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-blueviolet)](https://github.com/openai/codex)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

在手机上用 Codex 改应用，最大的卡点不是写代码，是看不到效果。Go Live 让每次改动自动部署上线，给你一条手机直接能打开的链接。Vibe coding，从“写完”到“看到”，中间不再断。

中文 | [English](README_EN.md)

</div>

---

## 怎么安装

如果你在 CLI 里使用 Codex：

```bash
npx skills add Sac-Y/go-live
```

如果你在 Codex App 或 ChatGPT 移动端里使用 Codex，直接对 Codex 说：

```text
请帮我安装这个 skill：
https://github.com/Sac-Y/go-live
```

---

## 如何使用

Go Live 不绑定某个部署平台。Codex 会先看项目已有部署方式，优先沿用现有平台；如果需要 Vercel、Cloudflare、GitHub 等插件能力，会在执行时再提示你安装或授权。

装好之后，在 Codex 里直接说：

```text
「帮我在手机上预览这个页面，改完后发我一个能打开的链接」
「这个网站我想边改边在手机上看，每次改完都帮我部署一下」
「做完这个前端改动后，帮我发一个公开预览链接」
```

它的工作方式很简单：

1. 先完成你要求的代码、内容或设计修改。
2. 运行项目里最快且有意义的检查，例如 build、lint、typecheck 或 smoke test。
3. 使用项目已有的部署方式，优先走 Vercel、Netlify、Cloudflare、Firebase、GitHub Pages 或项目自己的 CI/CD。
4. 部署完成后打开公开 URL，确认页面能访问，也能看到这次修改。
5. 最后回复你公开链接、改了什么，以及验证结果。

需要注意：

- 不要只给 localhost，除非你明确要求只做本地预览。
- 如果项目已经绑定了 Vercel 或其他部署平台，就继续用现有平台，不要临时另起一套。
- 如果部署需要登录、项目绑定、环境变量或 commit/push，Codex 会说明阻塞点，并告诉你下一步该怎么处理。
- 在公开 URL 真正检查通过前，不应该声称部署成功。

---

## License

MIT
