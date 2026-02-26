# E2E Test Automation Skill

自动化端到端测试技能包，用于 Web 应用的自动化测试执行。

## 功能特性

- ✅ 自动解析 Markdown 格式的测试用例
- 🌐 自动启动 Chrome 浏览器执行测试
- 📸 失败时自动截图保存证据
- 📊 生成详细的测试报告（Markdown/HTML/JSON）
- 🎯 支持性能指标验证
- 🐛 自动识别和标记 Bug 严重程度
- 📝 收集控制台错误和网络日志

## 安装依赖

### 基础依赖

```bash
pip install playwright asyncio
playwright install chromium
```

### 可选依赖

```bash
# 如果需要视频录制
pip install opencv-python

# 如果需要高级报告功能
pip install jinja2
```

## 使用方法

### 方法 1: 通过 Cursor Agent 使用（推荐）

在 Cursor 中直接对话：

```
根据 @e2e-test.md 的测试用例，自动执行所有测试并生成报告
```

Agent 会自动：
1. 读取测试用例文件
2. 启动浏览器
3. 执行所有测试
4. 生成测试报告

### 方法 2: 直接运行脚本

```bash
# 基本使用
python scripts/execute_tests.py path/to/test_cases.md

# 无头模式（后台运行）
python scripts/execute_tests.py path/to/test_cases.md --headless
```

## 测试用例格式

测试用例应该使用以下 Markdown 格式：

```markdown
测试网址：https://your-app.com
测试账号密码：username / password

---

1. 测试用例标题
- 操作步骤
  - 步骤 1
  - 步骤 2
  - 步骤 3
- 预期反馈
  - 预期结果 1
  - 预期结果 2
- 常见问题
  - 常见问题 1
  - 常见问题 2
```

## 测试报告

测试执行完成后会生成：

### 1. Markdown 报告
详细的测试报告，包含：
- 测试摘要统计
- 通过的测试用例
- 失败的测试用例（含截图）
- Bug 汇总（按严重程度分类）
- 性能指标
- 改进建议

### 2. HTML 报告
可视化的测试报告，可在浏览器中查看，包含图表和交互式元素。

### 3. JSON 报告
结构化数据，便于集成到 CI/CD 流程或其他工具。

## 输出目录结构

```
test_results/
├── screenshots/           # 测试截图
│   ├── test_1_failure.png
│   └── test_5_failure.png
├── videos/               # 测试录像（如果启用）
│   └── test_session.webm
├── logs/                 # 日志文件
│   ├── console_logs.txt
│   └── network_logs.json
└── report_20260115_143022.md  # 测试报告
```

## 高级功能

### 自定义测试执行

可以通过修改 `execute_tests.py` 来自定义测试行为：

```python
# 修改超时时间
config.timeout = 120000  # 120秒

# 启用视频录制
config.record_video = True

# 自定义浏览器选项
config.browser_options = {
    'headless': False,
    'slow_mo': 100  # 慢动作模式，便于观察
}
```

### 性能监控

自动收集性能指标：
- 页面加载时间
- API 响应时间
- 资源加载统计
- 内存使用情况

### 可访问性检查

基础可访问性检查：
- 图片 alt 文本
- 表单 label 标签
- ARIA 属性
- 键盘导航

## 故障排除

### 问题：Playwright 未安装

```bash
pip install playwright
playwright install chromium
```

### 问题：浏览器无法启动

- 确保已安装 Chromium：`playwright install chromium`
- 尝试使用有头模式：删除 `--headless` 参数
- 检查系统依赖：`playwright install-deps`

### 问题：元素选择器失效

参考 `references/browser_selectors.md` 获取最佳实践。

### 问题：测试超时

增加超时时间：

```python
config.timeout = 120000  # 从 60 秒增加到 120 秒
```

## 集成到 CI/CD

### GitHub Actions

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install playwright
          playwright install --with-deps chromium
      - name: Run E2E tests
        run: |
          python scripts/execute_tests.py test_cases.md --headless
      - name: Upload test results
        uses: actions/upload-artifact@v2
        if: always()
        with:
          name: test-results
          path: test_results/
```

## 最佳实践

1. **测试隔离**：每个测试用例应该独立，不依赖其他测试的状态
2. **显式等待**：使用显式等待而不是硬编码的 sleep
3. **清晰的断言**：每个验证都应该有明确的期望值
4. **证据收集**：失败时始终保存截图和日志
5. **描述性失败消息**：失败消息应该帮助开发者快速定位问题

## 参考文档

- `references/default_test_cases.md` - 测试用例模板和示例
- `references/browser_selectors.md` - 浏览器元素选择器最佳实践
- `references/test_report_template.md` - 测试报告模板

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 支持

如有问题，请查看：
1. 本 README 的故障排除部分
2. `references/` 目录下的参考文档
3. Playwright 官方文档：https://playwright.dev
