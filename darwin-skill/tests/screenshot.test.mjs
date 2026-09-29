import assert from 'node:assert/strict';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const scriptPath = fileURLToPath(new URL('../scripts/screenshot.mjs', import.meta.url));

test('loads Playwright through standard Node module resolution', async (context) => {
  const tempRoot = await mkdtemp(path.join(os.tmpdir(), 'darwin-screenshot-'));
  context.after(() => rm(tempRoot, { recursive: true, force: true }));

  const moduleRoot = path.join(tempRoot, 'node_modules', 'playwright');
  await mkdir(moduleRoot, { recursive: true });
  await writeFile(
    path.join(moduleRoot, 'index.js'),
    "module.exports = { chromium: { launch: async () => { throw new Error('portable-playwright-loaded'); } } };\n",
  );

  const htmlPath = path.join(tempRoot, 'card.html');
  const outputPath = path.join(tempRoot, 'card.png');
  await writeFile(htmlPath, '<div class="card">test</div>\n');

  const result = spawnSync(process.execPath, [scriptPath, htmlPath, outputPath], {
    encoding: 'utf8',
    env: {
      ...process.env,
      NODE_PATH: path.join(tempRoot, 'node_modules'),
    },
  });

  assert.equal(result.status, 1);
  assert.match(result.stderr, /portable-playwright-loaded/);
  assert.doesNotMatch(result.stderr, /Users\/alchain/);
});

test('keeps a successful screenshot when no output opener exists', async (context) => {
  const tempRoot = await mkdtemp(path.join(os.tmpdir(), 'darwin-screenshot-'));
  context.after(() => rm(tempRoot, { recursive: true, force: true }));

  const moduleRoot = path.join(tempRoot, 'node_modules', 'playwright');
  await mkdir(moduleRoot, { recursive: true });
  await writeFile(
    path.join(moduleRoot, 'index.js'),
    [
      "const fs = require('node:fs');",
      "module.exports = { chromium: { launch: async () => ({",
      "  newContext: async () => ({ newPage: async () => ({",
      "    goto: async () => {}, evaluate: async () => {}, waitForTimeout: async () => {},",
      "    locator: () => ({ screenshot: async ({ path }) => fs.writeFileSync(path, 'png'), boundingBox: async () => ({ width: 10, height: 20 }) }),",
      "  }) }),",
      "  close: async () => {},",
      "}) } };",
      "",
    ].join('\n'),
  );

  const htmlPath = path.join(tempRoot, 'card.html');
  const outputPath = path.join(tempRoot, 'card.png');
  await writeFile(htmlPath, '<div class="card">test</div>\n');

  const result = spawnSync(process.execPath, [scriptPath, htmlPath, outputPath], {
    encoding: 'utf8',
    env: {
      ...process.env,
      NODE_PATH: path.join(tempRoot, 'node_modules'),
      PATH: tempRoot,
    },
  });

  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /截图完成/);
  assert.equal(await readFile(outputPath, 'utf8'), 'png');
});
