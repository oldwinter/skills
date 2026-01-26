#!/usr/bin/env python3
"""
Obsidian Vault Analyzer
Generates comprehensive statistics and dashboard for Obsidian vaults
"""

import os
import json
import re
import glob
from datetime import datetime
from pathlib import Path
from collections import defaultdict, Counter
import argparse

class VaultAnalyzer:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path).resolve()
        self.stats = {
            'files': defaultdict(int),
            'tags': defaultdict(int),
            'links': {'internal': 0, 'external': 0, 'broken': 0},
            'folders': defaultdict(int),
            'attachments': defaultdict(int),
            'metadata': {}
        }
        self.file_details = []
        self.tag_hierarchy = defaultdict(set)
        self.link_map = defaultdict(set)
        self.orphaned_files = set()

    def analyze(self):
        """Main analysis function"""
        print(f"Analyzing vault at: {self.vault_path}")

        # Scan all files
        self._scan_files()

        # Analyze markdown files
        self._analyze_markdown_files()

        # Find orphaned files
        self._find_orphaned_files()

        # Calculate folder statistics
        self._calculate_folder_stats()

        # Generate reports
        self._generate_json_report()
        self._generate_html_dashboard()
        self._generate_markdown_report()

        print(f"Analysis complete! Check dashboard.html for results.")

    def _scan_files(self):
        """Scan all files in vault"""
        for file_path in self.vault_path.rglob('*'):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                self.stats['files']['total'] += 1
                self.stats['files'][ext] += 1

                # Track attachments
                if ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf',
                          '.mp4', '.webm', '.mp3', '.wav', '.m4a']:
                    self.stats['attachments'][ext] += 1

                # File details
                stat = file_path.stat()
                self.file_details.append({
                    'path': str(file_path.relative_to(self.vault_path)),
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'extension': ext
                })

    def _analyze_markdown_files(self):
        """Analyze markdown files for tags and links"""
        md_files = list(self.vault_path.rglob('*.md'))

        for md_file in md_files:
            content = md_file.read_text(encoding='utf-8', errors='ignore')

            # Extract tags
            tags = re.findall(r'#([\w/-]+)', content)
            for tag in tags:
                self.stats['tags'][tag] += 1
                # Build tag hierarchy
                parts = tag.split('/')
                for i in range(len(parts)):
                    parent = '/'.join(parts[:i+1])
                    if i < len(parts) - 1:
                        self.tag_hierarchy[parent].add(parts[i+1])

            # Extract links
            internal_links = re.findall(r'\[\[([^\]]+)\]\]', content)
            external_links = re.findall(r'\[([^\]]*)\]\((https?://[^\)]+)\)', content)

            self.stats['links']['internal'] += len(internal_links)
            self.stats['links']['external'] += len(external_links)

            # Track link destinations
            for link in internal_links:
                link_path = link.split('|')[0].split('#')[0]
                self.link_map[link_path].add(str(md_file.relative_to(self.vault_path)))

    def _find_orphaned_files(self):
        """Find files that are not referenced anywhere"""
        all_files = set()
        referenced_files = set()

        # Get all markdown files
        for md_file in self.vault_path.rglob('*.md'):
            all_files.add(md_file.stem)

        # Get referenced files
        for link in self.link_map:
            referenced_files.add(link)

        # Find orphaned attachments
        for file_path in self.vault_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf']:
                # Check if this attachment is referenced in any markdown file
                attachment_name = file_path.name
                is_referenced = False

                for md_file in self.vault_path.rglob('*.md'):
                    content = md_file.read_text(encoding='utf-8', errors='ignore')
                    if attachment_name in content or file_path.stem in content:
                        is_referenced = True
                        break

                if not is_referenced:
                    self.orphaned_files.add(str(file_path.relative_to(self.vault_path)))

    def _calculate_folder_stats(self):
        """Calculate folder statistics"""
        for file_info in self.file_details:
            folder = os.path.dirname(file_info['path'])
            while folder:
                self.stats['folders'][folder] += 1
                folder = os.path.dirname(folder)

    def _generate_json_report(self):
        """Generate JSON report"""
        report = {
            'summary': {
                'total_files': self.stats['files']['total'],
                'markdown_files': self.stats['files']['.md'],
                'attachments': sum(self.stats['attachments'].values()),
                'unique_tags': len(self.stats['tags']),
                'internal_links': self.stats['links']['internal'],
                'external_links': self.stats['links']['external'],
                'orphaned_files': len(self.orphaned_files)
            },
            'file_types': dict(self.stats['files']),
            'attachment_types': dict(self.stats['attachments']),
            'tag_usage': dict(sorted(self.stats['tags'].items(), key=lambda x: x[1], reverse=True)[:50]),
            'folder_distribution': dict(sorted(self.stats['folders'].items(), key=lambda x: x[1], reverse=True)),
            'orphaned_files': list(self.orphaned_files),
            'file_details': sorted(self.file_details, key=lambda x: x['modified'], reverse=True)[:100],
            'generated_at': datetime.now().isoformat()
        }

        with open('vault_stats.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

    def _generate_html_dashboard(self):
        """Generate interactive HTML dashboard"""
        html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Obsidian Vault Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        h1 {
            text-align: center;
            margin-bottom: 30px;
            color: #2c3e50;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }

        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            color: #3498db;
            margin-bottom: 5px;
        }

        .stat-label {
            color: #7f8c8d;
            font-size: 0.9em;
        }

        .chart-container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }

        .chart-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .file-list {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }

        .file-list h3 {
            margin-bottom: 15px;
            color: #2c3e50;
        }

        .file-list ul {
            list-style: none;
            max-height: 300px;
            overflow-y: auto;
        }

        .file-list li {
            padding: 8px;
            border-bottom: 1px solid #ecf0f1;
            font-family: monospace;
            font-size: 0.9em;
        }

        .tag-cloud {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
        }

        .tag {
            background: #3498db;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9em;
        }

        .orphan-warning {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Obsidian Vault Dashboard</h1>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_files}</div>
                <div class="stat-label">Total Files</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{md_files}</div>
                <div class="stat-label">Markdown Files</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{attachments}</div>
                <div class="stat-label">Attachments</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{tags}</div>
                <div class="stat-label">Unique Tags</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{int_links}</div>
                <div class="stat-label">Internal Links</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{orphaned}</div>
                <div class="stat-label">Orphaned Files</div>
            </div>
        </div>

        {orphan_warning}

        <div class="chart-grid">
            <div class="chart-container">
                <canvas id="fileTypeChart"></canvas>
            </div>
            <div class="chart-container">
                <canvas id="attachmentChart"></canvas>
            </div>
        </div>

        <div class="chart-container">
            <canvas id="tagChart"></canvas>
        </div>

        <div class="file-list">
            <h3>Recent Files</h3>
            <ul>
                {recent_files}
            </ul>
        </div>

        {orphan_files_section}
    </div>

    <script>
        // Load data
        const data = {data_json};

        // File Type Chart
        const fileTypeCtx = document.getElementById('fileTypeChart').getContext('2d');
        new Chart(fileTypeCtx, {{
            type: 'doughnut',
            data: {{
                labels: {file_type_labels},
                datasets: [{{
                    data: {file_type_data},
                    backgroundColor: [
                        '#3498db', '#2ecc71', '#e74c3c', '#f39c12',
                        '#9b59b6', '#1abc9c', '#34495e', '#95a5a6'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'File Type Distribution'
                    }}
                }}
            }}
        }});

        // Attachment Chart
        const attachmentCtx = document.getElementById('attachmentChart').getContext('2d');
        new Chart(attachmentCtx, {{
            type: 'bar',
            data: {{
                labels: {attachment_labels},
                datasets: [{{
                    label: 'Count',
                    data: {attachment_data},
                    backgroundColor: '#3498db'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'Attachment Types'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});

        // Tag Chart
        const tagCtx = document.getElementById('tagChart').getContext('2d');
        new Chart(tagCtx, {{
            type: 'bar',
            data: {{
                labels: {tag_labels},
                datasets: [{{
                    label: 'Usage Count',
                    data: {tag_data},
                    backgroundColor: '#2ecc71'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'Top Tags'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>'''

        # Load stats
        with open('vault_stats.json', 'r') as f:
            stats = json.load(f)

        # Prepare data for charts
        file_types = {k: v for k, v in stats['file_types'].items() if k != 'total' and k != '.md'}
        file_type_labels = list(file_types.keys())[:8]
        file_type_data = list(file_types.values())[:8]

        attachment_labels = list(stats['attachment_types'].keys())
        attachment_data = list(stats['attachment_types'].values())

        tag_labels = list(stats['tag_usage'].keys())[:15]
        tag_data = list(stats['tag_usage'].values())[:15]

        # Recent files
        recent_files = ''
        for file_info in stats['file_details'][:10]:
            recent_files += f'<li>{file_info["path"]} - {file_info["modified"][:10]}</li>'

        # Orphaned files warning
        orphan_warning = ''
        if stats['summary']['orphaned_files'] > 0:
            orphan_warning = f'''
            <div class="orphan-warning">
                <strong>Warning:</strong> Found {stats['summary']['orphaned_files']} orphaned files.
                These files are not referenced anywhere in your vault.
            </div>'''

        # Orphaned files section
        orphan_files_section = ''
        if stats['orphaned_files']:
            orphan_files_section = f'''
            <div class="file-list">
                <h3>Orphaned Files</h3>
                <ul>
                    {''.join([f'<li>{f}</li>' for f in stats['orphaned_files'][:20]])}
                </ul>
            </div>'''

        # Fill template
        html = html_template.format(
            total_files=stats['summary']['total_files'],
            md_files=stats['file_types'].get('.md', 0),
            attachments=stats['summary']['attachments'],
            tags=stats['summary']['unique_tags'],
            int_links=stats['summary']['internal_links'],
            ext_links=stats['summary']['external_links'],
            orphaned=stats['summary']['orphaned_files'],
            file_type_labels=json.dumps(file_type_labels),
            file_type_data=json.dumps(file_type_data),
            attachment_labels=json.dumps(attachment_labels),
            attachment_data=json.dumps(attachment_data),
            tag_labels=json.dumps(tag_labels),
            tag_data=json.dumps(tag_data),
            recent_files=recent_files,
            orphan_warning=orphan_warning,
            orphan_files_section=orphan_files_section,
            data_json=json.dumps(stats)
        )

        with open('dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html)

    def _generate_markdown_report(self):
        """Generate markdown summary report"""
        with open('vault_stats.json', 'r') as f:
            stats = json.load(f)

        report = f"""# Obsidian Vault Report

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Total Files**: {stats['summary']['total_files']}
- **Markdown Files**: {stats['file_types'].get('.md', 0)}
- **Attachments**: {stats['summary']['attachments']}
- **Unique Tags**: {stats['summary']['unique_tags']}
- **Internal Links**: {stats['summary']['internal_links']}
- **External Links**: {stats['summary']['external_links']}
- **Orphaned Files**: {stats['summary']['orphaned_files']}

## File Types

"""

        for ext, count in sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True)[:10]:
            if ext != 'total':
                report += f"- `{ext}`: {count} files\n"

        report += "\n## Top Tags\n\n"

        for tag, count in sorted(stats['tag_usage'].items(), key=lambda x: x[1], reverse=True)[:15]:
            report += f"- `#{tag}`: used {count} times\n"

        if stats['orphaned_files']:
            report += f"\n## Orphaned Files ({len(stats['orphaned_files'])} total)\n\n"
            for file in stats['orphaned_files'][:20]:
                report += f"- {file}\n"

        with open('vault_report.md', 'w', encoding='utf-8') as f:
            f.write(report)


def main():
    parser = argparse.ArgumentParser(description='Analyze Obsidian vault and generate dashboard')
    parser.add_argument('vault_path', help='Path to Obsidian vault')
    args = parser.parse_args()

    analyzer = VaultAnalyzer(args.vault_path)
    analyzer.analyze()


if __name__ == '__main__':
    main()