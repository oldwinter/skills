#!/usr/bin/env python3
"""
Download all Lenny Skills from refoundai.com using BeautifulSoup
"""
import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from html.parser import HTMLParser
from html import unescape

# All 87 Lenny skills
SKILLS = [
    {"name": "Writing North Star Metrics", "category": "Product Management", "skillUrl": "/lenny-skills/s/writing-north-star-metrics"},
    {"name": "Defining Product Vision", "category": "Product Management", "skillUrl": "/lenny-skills/s/defining-product-vision"},
    {"name": "Prioritizing Roadmap", "category": "Product Management", "skillUrl": "/lenny-skills/s/prioritizing-roadmap"},
    {"name": "Setting OKRs & Goals", "category": "Product Management", "skillUrl": "/lenny-skills/s/setting-okrs-goals"},
    {"name": "Competitive Analysis", "category": "Product Management", "skillUrl": "/lenny-skills/s/competitive-analysis"},
    {"name": "Writing PRDs", "category": "Product Management", "skillUrl": "/lenny-skills/s/writing-prds"},
    {"name": "Problem Definition", "category": "Product Management", "skillUrl": "/lenny-skills/s/problem-definition"},
    {"name": "Writing Specs & Designs", "category": "Product Management", "skillUrl": "/lenny-skills/s/writing-specs-designs"},
    {"name": "Scoping & Cutting", "category": "Product Management", "skillUrl": "/lenny-skills/s/scoping-cutting"},
    {"name": "Working Backwards", "category": "Product Management", "skillUrl": "/lenny-skills/s/working-backwards"},
    {"name": "Conducting User Interviews", "category": "Product Management", "skillUrl": "/lenny-skills/s/conducting-user-interviews"},
    {"name": "Designing Surveys", "category": "Product Management", "skillUrl": "/lenny-skills/s/designing-surveys"},
    {"name": "Analyzing User Feedback", "category": "Product Management", "skillUrl": "/lenny-skills/s/analyzing-user-feedback"},
    {"name": "Usability Testing", "category": "Product Management", "skillUrl": "/lenny-skills/s/usability-testing"},
    {"name": "Shipping Products", "category": "Product Management", "skillUrl": "/lenny-skills/s/shipping-products"},
    {"name": "Managing Timelines", "category": "Product Management", "skillUrl": "/lenny-skills/s/managing-timelines"},
    {"name": "Developing Product Taste", "category": "Product Management", "skillUrl": "/lenny-skills/s/product-taste-intuition"},
    {"name": "Product Operations", "category": "Product Management", "skillUrl": "/lenny-skills/s/product-operations"},
    {"name": "Behavioral Product Design", "category": "Product Management", "skillUrl": "/lenny-skills/s/behavioral-product-design"},
    {"name": "Startup Ideation", "category": "Product Management", "skillUrl": "/lenny-skills/s/startup-ideation"},
    {"name": "Dogfooding", "category": "Product Management", "skillUrl": "/lenny-skills/s/dogfooding"},
    {"name": "Startup Pivoting", "category": "Product Management", "skillUrl": "/lenny-skills/s/startup-pivoting"},
    {"name": "Writing Job Descriptions", "category": "Hiring & Teams", "skillUrl": "/lenny-skills/s/writing-job-descriptions"},
    {"name": "Conducting Interviews", "category": "Hiring & Teams", "skillUrl": "/lenny-skills/s/conducting-interviews"},
    {"name": "Evaluating Candidates", "category": "Hiring & Teams", "skillUrl": "/lenny-skills/s/evaluating-candidates"},
    {"name": "Onboarding New Hires", "category": "Hiring & Teams", "skillUrl": "/lenny-skills/s/onboarding-new-hires"},
    {"name": "Building Team Culture", "category": "Hiring & Teams", "skillUrl": "/lenny-skills/s/building-team-culture"},
    {"name": "Designing Team Rituals", "category": "Hiring & Teams", "skillUrl": "/lenny-skills/s/team-rituals"},
    {"name": "Running Effective 1:1s", "category": "Leadership", "skillUrl": "/lenny-skills/s/running-effective-1-1s"},
    {"name": "Having Difficult Conversations", "category": "Leadership", "skillUrl": "/lenny-skills/s/having-difficult-conversations"},
    {"name": "Delegating Work", "category": "Leadership", "skillUrl": "/lenny-skills/s/delegating-work"},
    {"name": "Managing Up", "category": "Leadership", "skillUrl": "/lenny-skills/s/managing-up"},
    {"name": "Running Decision Processes", "category": "Leadership", "skillUrl": "/lenny-skills/s/running-decision-processes"},
    {"name": "Planning Under Uncertainty", "category": "Leadership", "skillUrl": "/lenny-skills/s/planning-under-uncertainty"},
    {"name": "Evaluating Trade-offs", "category": "Leadership", "skillUrl": "/lenny-skills/s/evaluating-trade-offs"},
    {"name": "Post-mortems & Retrospectives", "category": "Leadership", "skillUrl": "/lenny-skills/s/post-mortems-retrospectives"},
    {"name": "Cross-functional Collaboration", "category": "Leadership", "skillUrl": "/lenny-skills/s/cross-functional-collaboration"},
    {"name": "Systems Thinking", "category": "Leadership", "skillUrl": "/lenny-skills/s/systems-thinking"},
    {"name": "Energy Management", "category": "Leadership", "skillUrl": "/lenny-skills/s/energy-management"},
    {"name": "Coaching Product Managers", "category": "Leadership", "skillUrl": "/lenny-skills/s/coaching-pms"},
    {"name": "Organizational Design", "category": "Leadership", "skillUrl": "/lenny-skills/s/organizational-design"},
    {"name": "Organizational Transformation", "category": "Leadership", "skillUrl": "/lenny-skills/s/organizational-transformation"},
    {"name": "AI Product Strategy", "category": "AI & Technology", "skillUrl": "/lenny-skills/s/ai-product-strategy"},
    {"name": "Building with LLMs", "category": "AI & Technology", "skillUrl": "/lenny-skills/s/building-with-llms"},
    {"name": "Evaluating New Technology", "category": "AI & Technology", "skillUrl": "/lenny-skills/s/evaluating-new-technology"},
    {"name": "Platform Strategy", "category": "AI & Technology", "skillUrl": "/lenny-skills/s/platform-strategy"},
    {"name": "Vibe Coding", "category": "AI & Technology", "skillUrl": "/lenny-skills/s/vibe-coding"},
    {"name": "AI Evaluation (Evals)", "category": "AI & Technology", "skillUrl": "/lenny-skills/s/ai-evals"},
    {"name": "Giving Presentations", "category": "Communication", "skillUrl": "/lenny-skills/s/giving-presentations"},
    {"name": "Written Communication", "category": "Communication", "skillUrl": "/lenny-skills/s/written-communication"},
    {"name": "Stakeholder Alignment", "category": "Communication", "skillUrl": "/lenny-skills/s/stakeholder-alignment"},
    {"name": "Running Offsites", "category": "Communication", "skillUrl": "/lenny-skills/s/running-offsites"},
    {"name": "Running Effective Meetings", "category": "Communication", "skillUrl": "/lenny-skills/s/running-effective-meetings"},
    {"name": "Measuring Product-Market Fit", "category": "Growth", "skillUrl": "/lenny-skills/s/measuring-product-market-fit"},
    {"name": "Designing Growth Loops", "category": "Growth", "skillUrl": "/lenny-skills/s/designing-growth-loops"},
    {"name": "Pricing Strategy", "category": "Growth", "skillUrl": "/lenny-skills/s/pricing-strategy"},
    {"name": "Retention & Engagement", "category": "Growth", "skillUrl": "/lenny-skills/s/retention-engagement"},
    {"name": "Marketplace Liquidity Management", "category": "Growth", "skillUrl": "/lenny-skills/s/marketplace-liquidity"},
    {"name": "User Onboarding", "category": "Growth", "skillUrl": "/lenny-skills/s/user-onboarding"},
    {"name": "Positioning & Messaging", "category": "Marketing", "skillUrl": "/lenny-skills/s/positioning-messaging"},
    {"name": "Brand Storytelling", "category": "Marketing", "skillUrl": "/lenny-skills/s/brand-storytelling"},
    {"name": "Launch Marketing", "category": "Marketing", "skillUrl": "/lenny-skills/s/launch-marketing"},
    {"name": "Content Marketing", "category": "Marketing", "skillUrl": "/lenny-skills/s/content-marketing"},
    {"name": "Community Building", "category": "Marketing", "skillUrl": "/lenny-skills/s/community-building"},
    {"name": "Media Relations", "category": "Marketing", "skillUrl": "/lenny-skills/s/media-relations"},
    {"name": "Building a Promotion Case", "category": "Career", "skillUrl": "/lenny-skills/s/building-a-promotion-case"},
    {"name": "Negotiating Offers", "category": "Career", "skillUrl": "/lenny-skills/s/negotiating-offers"},
    {"name": "Finding Mentors & Sponsors", "category": "Career", "skillUrl": "/lenny-skills/s/finding-mentors-sponsors"},
    {"name": "Career Transitions", "category": "Career", "skillUrl": "/lenny-skills/s/career-transitions"},
    {"name": "Managing Imposter Syndrome", "category": "Career", "skillUrl": "/lenny-skills/s/managing-imposter-syndrome"},
    {"name": "Personal Productivity", "category": "Career", "skillUrl": "/lenny-skills/s/personal-productivity"},
    {"name": "Fundraising Strategy", "category": "Career", "skillUrl": "/lenny-skills/s/fundraising"},
    {"name": "Founder Sales", "category": "Sales & GTM", "skillUrl": "/lenny-skills/s/founder-sales"},
    {"name": "Building Sales Team", "category": "Sales & GTM", "skillUrl": "/lenny-skills/s/building-sales-team"},
    {"name": "Enterprise Sales", "category": "Sales & GTM", "skillUrl": "/lenny-skills/s/enterprise-sales"},
    {"name": "Partnership & BD", "category": "Sales & GTM", "skillUrl": "/lenny-skills/s/partnership-bd"},
    {"name": "Product-Led Sales Strategy", "category": "Sales & GTM", "skillUrl": "/lenny-skills/s/product-led-sales"},
    {"name": "Sales Compensation Design", "category": "Sales & GTM", "skillUrl": "/lenny-skills/s/sales-compensation"},
    {"name": "Sales Qualification", "category": "Sales & GTM", "skillUrl": "/lenny-skills/s/sales-qualification"},
    {"name": "Technical Roadmaps", "category": "Engineering", "skillUrl": "/lenny-skills/s/technical-roadmaps"},
    {"name": "Managing Tech Debt", "category": "Engineering", "skillUrl": "/lenny-skills/s/managing-tech-debt"},
    {"name": "Platform & Infrastructure", "category": "Engineering", "skillUrl": "/lenny-skills/s/platform-infrastructure"},
    {"name": "Engineering Culture", "category": "Engineering", "skillUrl": "/lenny-skills/s/engineering-culture"},
    {"name": "Design Engineering", "category": "Engineering", "skillUrl": "/lenny-skills/s/design-engineering"},
    {"name": "Design Systems", "category": "Design", "skillUrl": "/lenny-skills/s/design-systems"},
    {"name": "Running Design Reviews", "category": "Design", "skillUrl": "/lenny-skills/s/running-design-reviews"},
]

BASE_URL = "https://refoundai.com"

def slugify(text):
    """Convert skill name to directory name"""
    return text.lower().replace(" ", "-").replace("&", "and").replace(":", "").replace("(", "").replace(")", "").replace("'", "")

def download_page(url):
    """Download page using curl"""
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', url],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout
        return None
    except Exception as e:
        print(f"  Error downloading: {e}")
        return None

def extract_text_content(html):
    """
    Simple HTML text extraction
    This extracts plain text from HTML without requiring external libraries
    """
    if not html:
        return None

    # Remove script and style elements
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # Convert common HTML entities
    html = unescape(html)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html)

    # Clean up whitespace
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    return '\n\n'.join(lines)

def save_skill(skill, content):
    """Save skill to both locations"""
    slug = slugify(skill['name'])

    # Prepare directories
    repo_dir = Path(f"/Users/cdd/Code/myself/skills/lenny-skills/{slug}")
    local_dir = Path(f"/Users/cdd/.claude/skills/{slug}")

    for dir_path in [repo_dir, local_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)

        # Save SKILL.md
        skill_file = dir_path / "SKILL.md"
        with open(skill_file, 'w', encoding='utf-8') as f:
            f.write(f"# {skill['name']}\n\n")
            f.write(f"**Category:** {skill['category']}\n\n")
            f.write(f"**Source:** {BASE_URL}{skill['skillUrl']}\n\n")
            f.write("---\n\n")
            f.write(content)

    return True

def create_readme():
    """Create README with categorized skills"""
    categories = {}
    for skill in SKILLS:
        cat = skill["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(skill)

    readme_content = "# Lenny Skills\n\n"
    readme_content += f"A collection of {len(SKILLS)} product management and leadership skills from [Lenny's Newsletter](https://refoundai.com/lenny-skills/).\n\n"
    readme_content += "## Skills by Category\n\n"

    for category in sorted(categories.keys()):
        readme_content += f"### {category}\n\n"
        for skill in sorted(categories[category], key=lambda x: x["name"]):
            skill_slug = slugify(skill["name"])
            readme_content += f"- [{skill['name']}](./{skill_slug}/SKILL.md)\n"
        readme_content += "\n"

    readme_file = Path("/Users/cdd/Code/myself/skills/lenny-skills/README.md")
    readme_file.write_text(readme_content, encoding='utf-8')
    print(f"✓ Created README: {readme_file}")

def main():
    print(f"Starting download of {len(SKILLS)} Lenny skills...")
    print(f"Repository: /Users/cdd/Code/myself/skills/lenny-skills/")
    print(f"Local installation: /Users/cdd/.claude/skills/")
    print("-" * 60)

    success_count = 0
    failed_skills = []

    for i, skill in enumerate(SKILLS, 1):
        print(f"\n[{i}/{len(SKILLS)}] {skill['name']}...", end=" ")

        # Download page
        url = f"{BASE_URL}{skill['skillUrl']}"
        html = download_page(url)

        if html:
            # Extract content
            content = extract_text_content(html)

            if content:
                # Save to both locations
                if save_skill(skill, content):
                    success_count += 1
                    print("✓")
                else:
                    failed_skills.append(skill["name"])
                    print("✗ (save failed)")
            else:
                failed_skills.append(skill["name"])
                print("✗ (extraction failed)")
        else:
            failed_skills.append(skill["name"])
            print("✗ (download failed)")

        # Rate limiting
        time.sleep(0.8)

    print("\n" + "=" * 60)
    print(f"Download complete!")
    print(f"✓ Success: {success_count}/{len(SKILLS)}")

    if failed_skills:
        print(f"✗ Failed: {len(failed_skills)}")
        print("Failed skills:")
        for name in failed_skills:
            print(f"  - {name}")

    # Create README
    create_readme()

    print(f"\n✓ All done! Skills saved to:")
    print(f"  - /Users/cdd/Code/myself/skills/lenny-skills/")
    print(f"  - /Users/cdd/.claude/skills/")

if __name__ == "__main__":
    main()
