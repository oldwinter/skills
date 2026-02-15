#!/usr/bin/env python3
"""
Test report generation utilities
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any


class ReportGenerator:
    """Generates test execution reports in various formats"""
    
    @staticmethod
    def generate_markdown(
        test_results: Dict[str, Any],
        output_path: Path
    ):
        """Generate detailed markdown report"""
        
        # Extract data
        summary = test_results.get('summary', {})
        passed_cases = test_results.get('passed', [])
        failed_cases = test_results.get('failed', [])
        warning_cases = test_results.get('warnings', [])
        bugs = test_results.get('bugs', {})
        performance = test_results.get('performance', {})
        
        report = []
        
        # Header
        report.append("# E2E Test Execution Report\n")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append("---\n")
        
        # Summary
        report.append("## Test Summary\n")
        for key, value in summary.items():
            report.append(f"- **{key}**: {value}")
        report.append("")
        
        # Overall status
        pass_rate = summary.get('pass_rate', 0)
        if pass_rate == 100:
            status = "✅ ALL TESTS PASSED"
        elif pass_rate >= 80:
            status = "⚠️ MOST TESTS PASSED"
        else:
            status = "❌ MANY TESTS FAILED"
        report.append(f"## Overall Status: {status}\n")
        
        # Passed cases
        if passed_cases:
            report.append("## ✅ Passed Cases\n")
            report.append("| # | Test Case | Category | Duration |")
            report.append("|---|-----------|----------|----------|")
            for tc in passed_cases:
                report.append(
                    f"| {tc['id']} | {tc['title']} | {tc['category']} | {tc['duration']:.2f}s |"
                )
            report.append("")
        
        # Failed cases
        if failed_cases:
            report.append("## ❌ Failed Cases\n")
            for tc in failed_cases:
                report.append(f"### {tc['id']}. {tc['title']}\n")
                report.append(f"- **Category**: {tc['category']}")
                report.append(f"- **Priority**: {tc['priority']}")
                report.append(f"- **Duration**: {tc['duration']:.2f}s")
                report.append(f"- **Severity**: {tc['severity']}")
                report.append(f"- **Reason**: {tc['reason']}\n")
                
                if tc.get('screenshot'):
                    report.append(f"**Screenshot**: `{tc['screenshot']}`\n")
                
                report.append("")
        
        # Warning cases
        if warning_cases:
            report.append("## ⚠️ Warning Cases\n")
            for tc in warning_cases:
                report.append(f"### {tc['id']}. {tc['title']}\n")
                report.append(f"- **Warning**: {tc['warning']}\n")
                report.append("")
        
        # Bugs summary
        if bugs:
            report.append("## Bugs and Issues Summary\n")
            
            for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
                issues = bugs.get(severity.lower(), [])
                if issues:
                    icon = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}[severity]
                    report.append(f"### {icon} {severity} Issues ({len(issues)})\n")
                    for i, issue in enumerate(issues, 1):
                        report.append(f"{i}. **{issue['title']}**")
                        report.append(f"   - Test Case: {issue['test_case']}")
                        report.append(f"   - Impact: {issue['impact']}")
                        report.append("")
        
        # Performance metrics
        if performance:
            report.append("## Performance Metrics\n")
            report.append("| Metric | Target | Actual | Status |")
            report.append("|--------|--------|--------|--------|")
            for metric in performance:
                status_icon = "✅" if metric['passed'] else "❌"
                report.append(
                    f"| {metric['name']} | {metric['target']} | "
                    f"{metric['actual']} | {status_icon} |"
                )
            report.append("")
        
        # Recommendations
        report.append("## Recommendations\n")
        report.append("### Immediate Actions\n")
        report.append("[List critical actions needed]\n")
        report.append("### Short-term Improvements\n")
        report.append("[List improvements to make]\n")
        
        # Write report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"📄 Markdown report saved: {output_path}")
    
    @staticmethod
    def generate_json(
        test_results: Dict[str, Any],
        output_path: Path
    ):
        """Generate JSON report for programmatic access"""
        
        # Add metadata
        test_results['metadata'] = {
            'generated_at': datetime.now().isoformat(),
            'report_version': '1.0'
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, indent=2)
        
        print(f"📄 JSON report saved: {output_path}")
    
    @staticmethod
    def generate_html(
        test_results: Dict[str, Any],
        output_path: Path
    ):
        """Generate HTML report with styling"""
        
        summary = test_results.get('summary', {})
        passed = len(test_results.get('passed', []))
        failed = len(test_results.get('failed', []))
        warnings = len(test_results.get('warnings', []))
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E2E Test Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2em;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
        }}
        .summary-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }}
        .passed {{ color: #22c55e; }}
        .failed {{ color: #ef4444; }}
        .warning {{ color: #f59e0b; }}
        .test-list {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .test-case {{
            border-left: 4px solid #ddd;
            padding: 10px;
            margin: 10px 0;
            background: #f9fafb;
        }}
        .test-case.pass {{ border-left-color: #22c55e; }}
        .test-case.fail {{ border-left-color: #ef4444; }}
        .test-case.warning {{ border-left-color: #f59e0b; }}
        .test-case h4 {{
            margin: 0 0 10px 0;
        }}
        .test-case .meta {{
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 E2E Test Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <div class="summary-card">
            <h3>Total Tests</h3>
            <div class="value">{summary.get('total', 0)}</div>
        </div>
        <div class="summary-card">
            <h3>Passed</h3>
            <div class="value passed">✅ {passed}</div>
        </div>
        <div class="summary-card">
            <h3>Failed</h3>
            <div class="value failed">❌ {failed}</div>
        </div>
        <div class="summary-card">
            <h3>Warnings</h3>
            <div class="value warning">⚠️ {warnings}</div>
        </div>
    </div>
    
    <div class="test-list">
        <h2>Test Results</h2>
"""
        
        # Add passed tests
        for tc in test_results.get('passed', []):
            html += f"""
        <div class="test-case pass">
            <h4>✅ {tc['id']}. {tc['title']}</h4>
            <div class="meta">
                Category: {tc['category']} | 
                Duration: {tc['duration']:.2f}s
            </div>
        </div>
"""
        
        # Add failed tests
        for tc in test_results.get('failed', []):
            html += f"""
        <div class="test-case fail">
            <h4>❌ {tc['id']}. {tc['title']}</h4>
            <div class="meta">
                Category: {tc['category']} | 
                Duration: {tc['duration']:.2f}s |
                Severity: {tc['severity']}
            </div>
            <p><strong>Reason:</strong> {tc['reason']}</p>
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"📄 HTML report saved: {output_path}")
    
    @staticmethod
    def generate_all_formats(
        test_results: Dict[str, Any],
        output_dir: Path
    ):
        """Generate reports in all formats"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Markdown
        ReportGenerator.generate_markdown(
            test_results,
            output_dir / f"report_{timestamp}.md"
        )
        
        # JSON
        ReportGenerator.generate_json(
            test_results,
            output_dir / f"report_{timestamp}.json"
        )
        
        # HTML
        ReportGenerator.generate_html(
            test_results,
            output_dir / f"report_{timestamp}.html"
        )
        
        print(f"\n✅ All reports generated in: {output_dir}")
