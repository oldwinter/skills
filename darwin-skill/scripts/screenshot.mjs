#!/usr/bin/env node
/**
 * Darwin Skill - 高清截图脚本
 *
 * 用法: node scripts/screenshot.mjs [html文件路径] [输出png路径]
 *
 * 特性:
 * - 2x deviceScaleFactor，输出高清图
 * - 只截 .card 元素，无多余背景
 * - 等待字体加载完成
 * - 截完后尝试用当前系统的图片打开命令打开文件
 */

import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);

const htmlPath = process.argv[2] || new URL('../templates/result-card.html', import.meta.url).pathname;
const outputPath = process.argv[3] || new URL('../templates/result-card.png', import.meta.url).pathname;

function loadPlaywright() {
  for (const packageName of ['playwright', 'playwright-core']) {
    try {
      return require(packageName);
    } catch (error) {
      if (error.code !== 'MODULE_NOT_FOUND') {
        throw error;
      }
    }
  }

  throw new Error('Playwright is required. Run npm install in the darwin-skill directory.');
}

function openOutput(filePath) {
  const opener = {
    darwin: ['open', [filePath]],
    linux: ['xdg-open', [filePath]],
    win32: ['cmd', ['/c', 'start', '', filePath]],
  }[process.platform];

  if (!opener) {
    return;
  }

  const child = spawn(opener[0], opener[1], { detached: true, stdio: 'ignore' });
  child.on('error', (error) => {
    console.warn('截图已生成，但无法自动打开: ' + error.message);
  });
  child.unref();
}

async function screenshot() {
  const pw = loadPlaywright();
  const browser = await pw.chromium.launch();

  try {
    const context = await browser.newContext({
      viewport: { width: 920, height: 1600 },
      deviceScaleFactor: 2,
    });

    const page = await context.newPage();

    await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'networkidle' });

    // 等待字体加载
    await page.evaluate(() => document.fonts.ready);
    // 额外等待确保渲染完成
    await page.waitForTimeout(2000);

    // 只截 .card 元素
    const card = await page.locator('.card');
    await card.screenshot({
      path: outputPath,
      type: 'png',
    });

    console.log(`截图完成: ${outputPath}`);

    // 获取图片尺寸信息
    const box = await card.boundingBox();
    console.log(`卡片尺寸: ${Math.round(box.width)}x${Math.round(box.height)}px (CSS)`);
    console.log(`输出尺寸: ${Math.round(box.width * 2)}x${Math.round(box.height * 2)}px (2x高清)`);

  } finally {
    await browser.close();
  }

  openOutput(outputPath);
}

screenshot().catch(err => {
  console.error('截图失败:', err.message);
  process.exit(1);
});
