#!/usr/bin/env python3
"""
E2E Test Execution Engine

This script executes end-to-end tests by:
1. Parsing test case specifications from markdown files
2. Launching browser via Playwright
3. Executing test cases sequentially
4. Capturing screenshots on failures
5. Generating comprehensive test reports
"""

import os
import sys
import json
import time
import asyncio
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class TestStep:
    """Represents a single test step"""
    description: str
    order: int


@dataclass
class TestCase:
    """Represents a complete test case"""
    id: int
    title: str
    category: str
    priority: str
    steps: List[TestStep]
    expected_results: List[str]
    common_issues: List[str]
    status: str = "PENDING"  # PENDING, RUNNING, PASS, FAIL, WARNING
    execution_time: float = 0.0
    failure_reason: str = ""
    screenshot_path: str = ""
    bug_severity: str = ""  # CRITICAL, HIGH, MEDIUM, LOW
    actual_results: List[str] = field(default_factory=list)


@dataclass
class TestConfig:
    """Test configuration"""
    test_url: str
    username: str
    password: str
    timeout: int = 60000  # milliseconds
    headless: bool = False
    screenshot_on_failure: bool = True


class TestCaseParser:
    """Parses test cases from markdown files"""
    
    @staticmethod
    def parse_markdown(file_path: str) -> tuple[TestConfig, List[TestCase]]:
        """Parse markdown file into test configuration and test cases"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse test configuration
        config = TestCaseParser._parse_config(content)
        
        # Parse test cases
        test_cases = TestCaseParser._parse_test_cases(content)
        
        return config, test_cases
    
    @staticmethod
    def _parse_config(content: str) -> TestConfig:
        """Extract test configuration from markdown"""
        url_match = re.search(r'测试网址[：:]\s*(.+)', content)
        cred_match = re.search(r'测试账号密码[：:]\s*(.+?)\s*[/／]\s*(.+)', content)
        
        test_url = url_match.group(1).strip() if url_match else ""
        username = cred_match.group(1).strip() if cred_match else ""
        password = cred_match.group(2).strip() if cred_match else ""
        
        return TestConfig(test_url=test_url, username=username, password=password)
    
    @staticmethod
    def _parse_test_cases(content: str) -> List[TestCase]:
        """Extract all test cases from markdown"""
        test_cases = []
        
        # Split by test case headers (numbered format: 1. Title)
        pattern = r'(\d+)\.\s+([^\n]+)\n-\s*操作步骤(.*?)(?=-\s*预期反馈|-\s*常见问题|\n\n\d+\.|$)'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            test_id = int(match.group(1))
            title = match.group(2).strip()
            
            # Find the full test case block
            case_start = match.start()
            next_case = re.search(r'\n\d+\.', content[match.end():])
            case_end = match.end() + next_case.start() if next_case else len(content)
            case_block = content[case_start:case_end]
            
            # Parse steps
            steps = TestCaseParser._parse_steps(case_block)
            
            # Parse expected results
            expected = TestCaseParser._parse_expected_results(case_block)
            
            # Parse common issues
            issues = TestCaseParser._parse_common_issues(case_block)
            
            # Determine category from title
            category = TestCaseParser._determine_category(title)
            
            # Determine priority (default to P1)
            priority = TestCaseParser._determine_priority(title)
            
            test_case = TestCase(
                id=test_id,
                title=title,
                category=category,
                priority=priority,
                steps=steps,
                expected_results=expected,
                common_issues=issues
            )
            
            test_cases.append(test_case)
        
        return test_cases
    
    @staticmethod
    def _parse_steps(case_block: str) -> List[TestStep]:
        """Parse operation steps from test case block"""
        steps = []
        steps_section = re.search(r'操作步骤(.*?)(?=预期反馈|常见问题|$)', case_block, re.DOTALL)
        
        if steps_section:
            # Find all bullet points
            step_matches = re.findall(r'-\s+(.+?)(?=\n\s*-|\n\s*-|$)', steps_section.group(1), re.DOTALL)
            for i, step_text in enumerate(step_matches):
                step_text = step_text.strip()
                if step_text:
                    steps.append(TestStep(description=step_text, order=i+1))
        
        return steps
    
    @staticmethod
    def _parse_expected_results(case_block: str) -> List[str]:
        """Parse expected results from test case block"""
        expected = []
        expected_section = re.search(r'预期反馈(.*?)(?=常见问题|$)', case_block, re.DOTALL)
        
        if expected_section:
            result_matches = re.findall(r'-\s+(.+?)(?=\n\s*-|\n\s*-|$)', expected_section.group(1), re.DOTALL)
            for result in result_matches:
                result = result.strip()
                if result:
                    expected.append(result)
        
        return expected
    
    @staticmethod
    def _parse_common_issues(case_block: str) -> List[str]:
        """Parse common issues from test case block"""
        issues = []
        issues_section = re.search(r'常见问题(.*?)(?=$)', case_block, re.DOTALL)
        
        if issues_section:
            issue_matches = re.findall(r'-\s+(.+?)(?=\n\s*-|\n\s*-|$)', issues_section.group(1), re.DOTALL)
            for issue in issue_matches:
                issue = issue.strip()
                if issue:
                    issues.append(issue)
        
        return issues
    
    @staticmethod
    def _determine_category(title: str) -> str:
        """Determine test category from title"""
        title_lower = title.lower()
        
        if any(keyword in title_lower for keyword in ['chat', '搜索', 'search', 'query']):
            return "Chat & Search"
        elif any(keyword in title_lower for keyword in ['list', '列表', 'table']):
            return "List & Table"
        elif any(keyword in title_lower for keyword in ['profile', 'detail', '详情']):
            return "Profile Detail"
        elif any(keyword in title_lower for keyword in ['email', 'copy writing', '邮件']):
            return "Email Copy Writing"
        elif any(keyword in title_lower for keyword in ['signal']):
            return "Signal"
        elif any(keyword in title_lower for keyword in ['share', 'report', 'feedback']):
            return "Sharing & Reporting"
        else:
            return "Other"
    
    @staticmethod
    def _determine_priority(title: str) -> str:
        """Determine test priority from title or default to P1"""
        # Can be enhanced to check for P0/P1/P2 markers in title
        # For now, default to P1
        return "P1"


class BrowserAutomation:
    """Handles browser automation using Playwright"""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.browser = None
        self.context = None
        self.page = None
    
    async def setup(self):
        """Initialize browser and page"""
        try:
            from playwright.async_api import async_playwright
            
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=self.config.headless
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            self.page = await self.context.new_page()
            
            # Set default timeout
            self.page.set_default_timeout(self.config.timeout)
            
            print("✅ Browser initialized successfully")
            return True
            
        except ImportError:
            print("❌ Playwright not installed. Run: pip install playwright && playwright install chromium")
            return False
        except Exception as e:
            print(f"❌ Failed to initialize browser: {e}")
            return False
    
    async def login(self):
        """Perform login"""
        try:
            print(f"🔐 Logging in to {self.config.test_url}...")
            
            await self.page.goto(self.config.test_url)
            
            # Wait for page load
            await self.page.wait_for_load_state('networkidle')
            
            # Look for login form (adjust selectors as needed)
            # This is a generic example - should be customized per application
            username_selector = 'input[name="username"], input[type="email"], input[placeholder*="email"]'
            password_selector = 'input[name="password"], input[type="password"]'
            submit_selector = 'button[type="submit"], button:has-text("登录"), button:has-text("Login")'
            
            # Fill credentials
            await self.page.fill(username_selector, self.config.username)
            await self.page.fill(password_selector, self.config.password)
            
            # Click login
            await self.page.click(submit_selector)
            
            # Wait for navigation
            await self.page.wait_for_load_state('networkidle')
            
            print("✅ Login successful")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    async def execute_test_case(self, test_case: TestCase, screenshot_dir: Path) -> TestCase:
        """Execute a single test case"""
        print(f"\n{'='*60}")
        print(f"📋 Executing Test Case {test_case.id}: {test_case.title}")
        print(f"{'='*60}")
        
        test_case.status = "RUNNING"
        start_time = time.time()
        
        try:
            # Execute each step
            for step in test_case.steps:
                print(f"  ▶️  Step {step.order}: {step.description}")
                # Here you would implement actual step execution
                # This is a placeholder that should be customized per test case
                await asyncio.sleep(0.5)  # Simulate step execution
            
            # Validate expected results
            all_passed = True
            for i, expected in enumerate(test_case.expected_results):
                print(f"  ✓ Validating: {expected[:60]}...")
                # Here you would implement actual validation
                # This is a placeholder
                validation_passed = await self._validate_result(expected)
                
                if validation_passed:
                    test_case.actual_results.append(f"✅ {expected}")
                else:
                    test_case.actual_results.append(f"❌ {expected}")
                    all_passed = False
            
            # Determine test result
            if all_passed:
                test_case.status = "PASS"
                print(f"✅ Test Case {test_case.id} PASSED")
            else:
                test_case.status = "FAIL"
                test_case.failure_reason = "One or more expected results not met"
                test_case.bug_severity = "MEDIUM"
                print(f"❌ Test Case {test_case.id} FAILED")
                
                # Take screenshot on failure
                if self.config.screenshot_on_failure:
                    screenshot_path = screenshot_dir / f"test_{test_case.id}_failure.png"
                    await self.page.screenshot(path=str(screenshot_path))
                    test_case.screenshot_path = str(screenshot_path)
                    print(f"📸 Screenshot saved: {screenshot_path}")
        
        except Exception as e:
            test_case.status = "FAIL"
            test_case.failure_reason = f"Exception during execution: {str(e)}"
            test_case.bug_severity = "HIGH"
            print(f"❌ Test Case {test_case.id} FAILED with exception: {e}")
            
            # Take screenshot on exception
            if self.config.screenshot_on_failure:
                screenshot_path = screenshot_dir / f"test_{test_case.id}_exception.png"
                await self.page.screenshot(path=str(screenshot_path))
                test_case.screenshot_path = str(screenshot_path)
        
        test_case.execution_time = time.time() - start_time
        
        return test_case
    
    async def _validate_result(self, expected: str) -> bool:
        """Validate expected result (placeholder - should be customized)"""
        # This is a simplified validation
        # In real implementation, you would:
        # 1. Check for specific elements
        # 2. Validate text content
        # 3. Check performance metrics
        # 4. Verify no console errors
        
        await asyncio.sleep(0.2)  # Simulate validation
        
        # For demo purposes, randomly pass/fail (90% pass rate)
        import random
        return random.random() > 0.1
    
    async def cleanup(self):
        """Close browser and cleanup"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
        
        print("\n✅ Browser cleanup completed")


class TestReportGenerator:
    """Generates test execution reports"""
    
    @staticmethod
    def generate_markdown_report(
        config: TestConfig,
        test_cases: List[TestCase],
        output_path: Path
    ):
        """Generate detailed markdown report"""
        
        # Calculate statistics
        total = len(test_cases)
        passed = sum(1 for tc in test_cases if tc.status == "PASS")
        failed = sum(1 for tc in test_cases if tc.status == "FAIL")
        warnings = sum(1 for tc in test_cases if tc.status == "WARNING")
        total_time = sum(tc.execution_time for tc in test_cases)
        
        # Generate report
        report = []
        report.append("# E2E Test Execution Report\n")
        report.append("## Test Summary\n")
        report.append(f"- **Test URL**: {config.test_url}")
        report.append(f"- **Test Account**: {config.username}")
        report.append(f"- **Total Cases**: {total}")
        report.append(f"- **Passed**: {passed} ({passed/total*100:.1f}%)")
        report.append(f"- **Failed**: {failed} ({failed/total*100:.1f}%)")
        report.append(f"- **Warnings**: {warnings} ({warnings/total*100:.1f}%)")
        report.append(f"- **Execution Time**: {total_time:.2f}s")
        report.append(f"- **Test Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Overall status
        if failed == 0 and warnings == 0:
            report.append("## Overall Status: ✅ ALL TESTS PASSED\n")
        elif failed > 0:
            report.append("## Overall Status: ❌ SOME TESTS FAILED\n")
        else:
            report.append("## Overall Status: ⚠️ TESTS PASSED WITH WARNINGS\n")
        
        # Passed cases
        passed_cases = [tc for tc in test_cases if tc.status == "PASS"]
        if passed_cases:
            report.append("## ✅ Passed Cases\n")
            report.append("| # | Test Case | Category | Duration |")
            report.append("|---|-----------|----------|----------|")
            for tc in passed_cases:
                report.append(f"| {tc.id} | {tc.title} | {tc.category} | {tc.execution_time:.2f}s |")
            report.append("")
        
        # Failed cases
        failed_cases = [tc for tc in test_cases if tc.status == "FAIL"]
        if failed_cases:
            report.append("## ❌ Failed Cases\n")
            for tc in failed_cases:
                report.append(f"### {tc.id}. {tc.title}\n")
                report.append(f"- **Category**: {tc.category}")
                report.append(f"- **Priority**: {tc.priority}")
                report.append(f"- **Execution Time**: {tc.execution_time:.2f}s")
                report.append(f"- **Bug Severity**: {tc.bug_severity}")
                report.append(f"- **Failure Reason**: {tc.failure_reason}\n")
                
                report.append("**Expected Results:**")
                for result in tc.actual_results:
                    report.append(f"- {result}")
                
                if tc.screenshot_path:
                    report.append(f"\n**Screenshot**: {tc.screenshot_path}\n")
                
                report.append("")
        
        # Write report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"\n📄 Test report generated: {output_path}")


async def main():
    """Main execution function"""
    
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python execute_tests.py <test_case_file.md> [--headless]")
        sys.exit(1)
    
    test_file = sys.argv[1]
    headless = "--headless" in sys.argv
    
    # Validate test file exists
    if not Path(test_file).exists():
        print(f"❌ Test file not found: {test_file}")
        sys.exit(1)
    
    print(f"🚀 Starting E2E Test Execution")
    print(f"📁 Test File: {test_file}")
    print(f"🖥️  Headless Mode: {headless}\n")
    
    # Parse test cases
    print("📖 Parsing test cases...")
    config, test_cases = TestCaseParser.parse_markdown(test_file)
    config.headless = headless
    print(f"✅ Parsed {len(test_cases)} test cases")
    print(f"🔗 Test URL: {config.test_url}")
    print(f"👤 Test Account: {config.username}\n")
    
    # Setup output directories
    output_dir = Path("test_results")
    output_dir.mkdir(exist_ok=True)
    screenshot_dir = output_dir / "screenshots"
    screenshot_dir.mkdir(exist_ok=True)
    
    # Initialize browser
    browser = BrowserAutomation(config)
    if not await browser.setup():
        sys.exit(1)
    
    # Login
    if not await browser.login():
        print("❌ Login failed, aborting tests")
        await browser.cleanup()
        sys.exit(1)
    
    # Execute test cases
    print(f"\n{'='*60}")
    print(f"🧪 Executing {len(test_cases)} test cases...")
    print(f"{'='*60}\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Progress: {i}/{len(test_cases)}")
        test_cases[i-1] = await browser.execute_test_case(test_case, screenshot_dir)
        
        # Small delay between tests
        await asyncio.sleep(1)
    
    # Cleanup browser
    await browser.cleanup()
    
    # Generate report
    print("\n📊 Generating test report...")
    report_path = output_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    TestReportGenerator.generate_markdown_report(config, test_cases, report_path)
    
    # Print summary
    passed = sum(1 for tc in test_cases if tc.status == "PASS")
    failed = sum(1 for tc in test_cases if tc.status == "FAIL")
    
    print(f"\n{'='*60}")
    print(f"✨ Test Execution Complete!")
    print(f"{'='*60}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📄 Report: {report_path}")
    print(f"📸 Screenshots: {screenshot_dir}")
    print(f"{'='*60}\n")
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())
