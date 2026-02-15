---
name: e2e-test-automation
description: This skill should be used when users need to automate end-to-end (E2E) testing for web applications. It automatically launches Chrome browser, executes test cases based on provided specifications, captures screenshots on failures, and generates comprehensive test reports. Use this skill when asked to run E2E tests, automate UI testing, validate web application functionality, or generate test execution reports.
---

# E2E Test Automation

## Overview

Automate end-to-end testing for web applications by launching Chrome/Chromium browser, executing predefined test cases, capturing evidence (screenshots/videos), and generating detailed test reports. This skill integrates with Cursor's built-in browser capabilities and MCP browser servers to provide seamless automated testing.

## Core Capabilities

### 1. Test Case Management
- Parse test case specifications from markdown files
- Support structured test case format with operation steps, expected results, and common issues
- Organize test cases by priority (P0, P1, P2) and category (functional, performance, usability)

### 2. Automated Browser Testing
- Launch Chrome/Chromium browser automatically using MCP browser servers
- Execute test cases sequentially with clear logging
- Support login/authentication flows
- Handle dynamic content loading and async operations
- Capture screenshots for each critical step

### 3. Intelligent Validation
- Verify expected outcomes against actual results
- Detect common issues: timeouts, missing elements, incorrect content, broken links
- Identify UX problems and potential bugs
- Validate performance metrics (loading time < 60s, etc.)

### 4. Comprehensive Reporting
- Generate structured test reports in markdown format
- Include pass/fail status, execution time, and failure reasons
- Attach screenshots for failed cases
- Highlight bugs and UX issues with severity levels
- Provide recommendations for fixes

## Workflow

### Step 1: Load Test Cases

Read test case specifications from the provided markdown file or reference. Test cases should follow this structure:

```markdown
## Test Case Title
- 操作步骤 (Operation Steps)
  - Step 1
  - Step 2
- 预期反馈 (Expected Results)
  - Expected outcome 1
  - Expected outcome 2
- 常见问题 (Common Issues)
  - Known issue 1
  - Known issue 2
```

If no test cases are provided, use the default test suite from `references/default_test_cases.md`.

### Step 2: Prepare Test Environment

1. Check if browser MCP servers are available:
   - `cursor-browser-extension`
   - `cursor-ide-browser`

2. Launch browser using the appropriate MCP server tools

3. If test requires authentication:
   - Navigate to login page
   - Input credentials (from test specification or user prompt)
   - Verify successful login

### Step 3: Execute Test Cases

For each test case:

1. **Navigate to target page**
   - Log the navigation action
   - Wait for page load completion

2. **Execute operation steps**
   - Follow each step in the test case
   - Handle dynamic elements (wait for visibility)
   - Capture screenshot after critical operations

3. **Validate expected results**
   - Check each expected outcome
   - Measure performance metrics (if specified)
   - Record actual vs expected differences

4. **Detect common issues**
   - Check for known problems listed in test case
   - Identify UX problems (confusing UI, missing feedback, etc.)
   - Note any unexpected behaviors

5. **Record results**
   - Status: PASS / FAIL / WARNING
   - Execution time
   - Failure reason (if failed)
   - Screenshots (if failed or warning)
   - Bug severity: CRITICAL / HIGH / MEDIUM / LOW

### Step 4: Generate Test Report

Create a comprehensive test report with the following sections:

```markdown
# E2E Test Execution Report

## Test Summary
- Test URL: [URL]
- Test Account: [Account]
- Total Cases: [N]
- Passed: [N]
- Failed: [N]
- Warnings: [N]
- Execution Time: [Duration]
- Test Date: [Timestamp]

## Test Environment
- Browser: Chrome/Chromium
- Test Tool: Cursor MCP Browser
- Test Executor: [Executor Name]

## Detailed Results

### ✅ Passed Cases ([N])
[List of passed cases with brief description]

### ❌ Failed Cases ([N])
#### Case: [Test Case Title]
- **Status**: FAIL
- **Execution Time**: [Duration]
- **Failure Reason**: [Detailed reason]
- **Expected**: [What was expected]
- **Actual**: [What actually happened]
- **Screenshot**: [Path or embedded image]
- **Bug Severity**: [CRITICAL/HIGH/MEDIUM/LOW]
- **Recommendation**: [How to fix]

### ⚠️ Warning Cases ([N])
[Cases that passed but have UX issues or concerns]

## Bugs and Issues Summary

### Critical Issues ([N])
1. [Issue description with case reference]

### High Priority Issues ([N])
1. [Issue description with case reference]

### Medium Priority Issues ([N])
1. [Issue description with case reference]

### Low Priority Issues ([N])
1. [Issue description with case reference]

## UX Feedback
[General UX observations and improvement suggestions]

## Recommendations
[Overall recommendations for improving quality]
```

### Step 5: Cleanup

- Close browser instances
- Save screenshots to appropriate directory
- Archive test artifacts

## Usage Examples

### Example 1: Run all test cases from specification

User: "根据 @e2e-test.md 的测试用例，自动执行所有测试并生成报告"

Actions:
1. Read test cases from `e2e-test.md`
2. Launch browser and navigate to test URL
3. Login with provided credentials
4. Execute all 28 test cases sequentially
5. Generate comprehensive test report

### Example 2: Run specific test categories

User: "只运行 Chat 相关的测试用例"

Actions:
1. Parse test cases and filter for Chat category
2. Execute filtered test cases
3. Generate focused report for Chat functionality

### Example 3: Quick smoke test

User: "执行 P0 优先级的测试用例"

Actions:
1. Filter for P0 priority cases (from `case-p0/p0.md`)
2. Execute critical path tests
3. Generate quick validation report

## Test Case Format

Test cases should be provided in markdown format following this structure:

```markdown
测试网址：[URL]
测试账号密码：[username] / [password]

---

1. [Test Case Title]
- 操作步骤
  - [Step 1]
  - [Step 2]
- 预期反馈
  - [Expected result 1]
  - [Expected result 2]
- 常见问题
  - [Common issue 1]
  - [Common issue 2]
```

## Performance Metrics

The skill automatically validates common performance requirements:
- Page load time < 60s
- Search/query response time < 60s
- Export/download completion < 30s
- No console errors during critical operations

## Error Handling

When test execution encounters errors:

1. **Timeout errors**: Capture screenshot, log timeout duration, mark as FAIL
2. **Element not found**: Capture DOM snapshot, suggest possible selectors, mark as FAIL
3. **Assertion failures**: Log expected vs actual, capture screenshot, mark as FAIL
4. **Unexpected errors**: Full error stack, screenshot, mark as FAIL with CRITICAL severity

## Browser Compatibility

Primary browser: Chrome/Chromium (via Cursor MCP browser servers)

If MCP browser servers are not available, the skill can alternatively:
- Use Playwright for browser automation
- Use Selenium WebDriver
- Guide user to install required dependencies

## Resources

### references/
- `default_test_cases.md`: Template and default test cases
- `test_report_template.md`: Standard report format
- `browser_selectors.md`: Common CSS selectors for web elements

### scripts/
- `execute_tests.py`: Main test execution engine (Python)
- `browser_automation.py`: Browser control utilities
- `report_generator.py`: Test report generation
- `screenshot_capture.py`: Screenshot and evidence capture

### assets/
- `test_report_styles.css`: Styling for HTML reports
- `icons/`: Status icons (pass/fail/warning)

## Integration with Cursor

This skill leverages Cursor's built-in capabilities:

1. **MCP Browser Servers**: Use `cursor-browser-extension` or `cursor-ide-browser` for browser automation
2. **File System**: Save test reports and screenshots to workspace
3. **Terminal**: Execute test scripts in background if needed
4. **Markdown Preview**: Display test reports directly in Cursor

## Best Practices

1. **Test Isolation**: Each test case should be independent and not rely on previous test state
2. **Explicit Waits**: Use explicit waits for dynamic content, avoid hard-coded sleeps
3. **Clear Assertions**: Each validation should have a clear expected vs actual comparison
4. **Evidence Collection**: Always capture screenshots for failures
5. **Descriptive Failures**: Failure messages should help developers quickly identify root cause
6. **Performance Monitoring**: Track and report slow operations even if they pass
7. **UX Observations**: Note confusing UI/UX even in passing tests

## Limitations

- Requires working internet connection for web application testing
- MCP browser servers must be available or Playwright/Selenium installed
- Cannot test mobile-specific behaviors (mobile browser simulation only)
- Limited support for testing file uploads/downloads (workarounds available)
- Cannot bypass CAPTCHA or advanced bot detection automatically

## Troubleshooting

**MCP browser not available:**
Run: `pip install playwright && playwright install chromium`

**Element selectors not working:**
Check `references/browser_selectors.md` for recommended selector strategies

**Tests timing out:**
Increase timeout thresholds in test case specifications or use more specific waits

**Screenshots not capturing:**
Verify write permissions in workspace directory
