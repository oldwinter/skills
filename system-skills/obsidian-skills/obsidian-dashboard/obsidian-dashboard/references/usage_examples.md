# Obsidian Dashboard Usage Examples

## Basic Usage

```bash
# Analyze your vault
python3 /Users/cdd/.claude/skills/obsidian-dashboard/scripts/analyze_vault.py /path/to/your/vault

# The script will generate three files:
# - dashboard.html (Interactive HTML dashboard)
# - vault_stats.json (Raw statistics data)
# - vault_report.md (Markdown summary)
```

## What the Dashboard Shows

### Summary Cards
- Total files in vault
- Number of markdown files
- Total attachments
- Unique tags count
- Internal/external links
- Orphaned files count

### Charts and Visualizations
1. **File Type Distribution** - Doughnut chart showing file extensions
2. **Attachment Types** - Bar chart of image, PDF, and media files
3. **Top Tags** - Most frequently used tags in your vault

### Lists and Details
- Recent files (last 100 modifications)
- Orphaned files (files not referenced anywhere)
- Top 50 most used tags
- Folder distribution statistics

## Advanced Features

### Finding Orphaned Files
The dashboard identifies files that exist in your vault but are not referenced anywhere:
- Orphaned images/media
- Unlinked PDFs
- Abandoned attachments

### Tag Analysis
- Hierarchical tag structure (e.g., #parent/child)
- Usage frequency for each tag
- Top 50 tags visualization

### Link Analysis
- Total internal links (wikilinks)
- External links to websites
- Tracks link destinations for navigation

## Tips for Large Vaults

For vaults with thousands of files:
- Analysis may take a few minutes
- The HTML dashboard loads progressively
- JSON data can be processed by other tools
- Markdown report provides quick overview

## Customization

The dashboard uses Chart.js for interactive visualizations and is fully self-contained (no external dependencies except for Chart.js CDN). You can:
- Save the HTML file for offline viewing
- Share the dashboard with others
- Customize the styling in the HTML template
- Process the JSON data with other tools