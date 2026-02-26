---
name: platform-and-infrastructure
description: Plan platform and infrastructure improvements for reliability, scale, and developer velocity.
---

# Platform & Infrastructure

**Category:** Engineering

**Source:** https://refoundai.com/lenny-skills/s/platform-infrastructure

---

Platform & Infrastructure | Refound AI

Lenny Skills Database     SKILLS  PLAYBOOKS  GUESTS  ABOUT               SKILLS  PLAYBOOKS  GUESTS  ABOUT                     Engineering   5 guests | 6 insights

Platform & Infrastructure  Platform and infrastructure work is the 'invisible' foundation that determines whether your product can scale. The best products often win on reliability, performance, and architecture rather than feature count. Infrastructure investments require anticipating 100X scale before you need it.

Download Claude Skill

Read Guide

The Guide  5 key steps synthesized from 5 experts.

1 Prioritize invisible qualities over visible features  The success of major platforms often depends on reliability, speed, privacy, and safety rather than feature count. WhatsApp won with end-to-end encryption and performance, not a feature-rich interface. Focus on the infrastructure qualities that build trust and enable scale.

Featured guest perspectives

"It wasn't the hundreds of features, it was all in the infrastructure and the platform... performance, reliability, privacy, safety, all of those things."

— Asha Sharma        2 Abstract common capabilities into shared infrastructure  Scaling feature velocity requires identifying repetitive components and building them into a core platform architecture. Standardize capabilities like data export, filtering, or permissions at the infrastructure level so developers only focus on unique product logic.

Featured guest perspectives

"We actually stopped for the first time and say, 'What is the column like?' And we also organized all the product architecture around it... we defined what is it, and then create an infrastructure for all these shared things, making the work of adding a new column just thinking about the specific product that you want to provide."

— Daniel Lereya        3 Set a 'doomsday clock' for scaling projects  While avoiding premature optimization is good, you need to monitor infrastructure limits and trigger scaling projects before failure. Know your breaking points (like running out of database capacity) and plan far enough ahead to avoid catastrophic outages during growth spikes.

Featured guest perspectives

"During COVID, we just couldn't scale up our infrastructure. For the longest time... we're running off even the largest instance there is for Postgres. So there's a doomsday clock... we just need to go as fast as you can to become sharding problem."

— Ivan Zhao        4 Dedicate top talent to 100X problems  Critical infrastructure projects require dedicated teams focused on long-term architectural shifts rather than incremental features. Isolate your most talented engineers to solve 100X scale problems that will provide competitive advantage, even if it means temporarily reducing feature output.

Featured guest perspectives

"We need few of our most talented people that are now not going to contribute features anymore. We are putting them on a separate place, and let's think and solve this problem while thinking about 100X."

— Daniel Lereya        5 Default to server-side tracking  For analytics and data infrastructure, server-side tracking is superior to client-side SDKs. It avoids data loss from ad-blockers, ensures cross-platform consistency, and reduces developer maintenance burden. Use server-side logs with user IDs as the primary source for behavioral events.

Featured guest perspectives

"The biggest mistake is setting up analytics using client side SDKs... start tracking events from your servers instead of from your clients."

— Vijay

✗ Common Mistakes

Competing on feature count when reliability and performance matter moreWaiting until infrastructure is failing to start scaling projectsBuilding the same capabilities repeatedly instead of abstracting them into platformRelying on client-side tracking that loses data to ad-blockers     ✓ Signs You're Doing It Well

New features ship faster because common capabilities are already solvedYou know your infrastructure breaking points and have projects to address them before they hitEnterprise customers trust you because of reliability and data residency, not just featuresYour top engineers are excited to work on foundational problems, not just shipping features

All Guest Perspectives

Deep dive into what all 5 guests shared about platform & infrastructure.

Asha Sharma 1 quote

Listen to episode →

"it wasn't the hundreds of features, it was all in the infrastructure and the platform... performance, reliability, privacy, safety, all of those things."  Tactical:  Prioritize reliability, speed, and end-to-end encryption in communication platformsFocus on data residency and availability to build trust with enterprise customers

View all skills from Asha Sharma →

Daniel Lereya 2 quotes

Listen to episode →

"We actually stopped for the first time and say, 'What is the column like?' And we also organized all the product architecture around it... we defined what is it, and then create an infrastructure for all these shared things, making the work of adding a new column just thinking about the specific product that you want to provide."  Tactical:  Identify repetitive feature components and build them into a core platform architectureStandardize capabilities like 'export to Excel' or 'filtering' at the infrastructure level    "We need few of our most talented people that are now not going to contribute features anymore. We are putting them on a separate place, and let's think and solve this problem while thinking about 100X."  Tactical:  Isolate top talent to work on long-term architectural shifts that provide a competitive edgeAnticipate infrastructure breaking points by planning for 100X current capacity

View all skills from Daniel Lereya →

Eli Schwartz 1 quote

Listen to episode →

"If you create a categorized sitemap where you can say, 'These are all the questions on health and from the sitemap... then a search engine can navigate through the entire site, and all of the questions and answers are discoverable.'"  Tactical:  Build a categorized HTML sitemap that allows bots to navigate the entire site depthImplement 'related content' links on every page to create a crawlable web for search engines

View all skills from Eli Schwartz →

Ivan Zhao 1 quote

Listen to episode →

"During COVID, we just couldn't scale up our infrastructure. For the longest time, Simon's really good at don't do premature optimization, so for the longest time, we Notion runs on one instance of Postgres database... we're running off even the largest instance there is for Postgres. So there's a doomsday clock... we just need to go as fast as you can to become sharding problem."  Tactical:  Monitor database limits and set a 'doomsday clock' to trigger scaling projects (like sharding) before failure.Be prepared to halt feature development to focus entirely on critical infrastructure scaling.

View all skills from Ivan Zhao →

Vijay 1 quote

Listen to episode →

"The biggest mistake is setting up analytics using client side SDKs... start tracking events from your servers instead of from your clients."  Tactical:  Default to server-side event tracking to avoid data loss from ad-blockersUse server-side logs with user IDs as the primary source for behavioral events

View all skills from Vijay →

Install This Skill

Add this skill to Claude Code, Cursor, or any AI coding assistant that supports Agent Skills.

1  Download the skill

Download SKILL.md

2  Add to your project

Create a folder in your project root and add the skill file:

.claude/skills/platform-infrastructure/SKILL.md    3  Start using it

Claude will automatically detect and use the skill when relevant. You can also invoke it directly:

Help me with platform & infrastructure              Related Skills Other Engineering skills you might find useful.    19 guests    Engineering Culture A high-performance engineering culture can be built around extreme experimentation frequency and tig...  View Skill → →      18 guests    Managing Tech Debt When a technical solution lacks the operational flexibility required by the business, a full rebuild...  View Skill → →      1 guests    Technical Roadmaps A written strategy is essential for organizational alignment and provides a baseline that can be cri...  View Skill → →      2 guests    Design Engineering The guest discusses the creation of a specific 'Design Engineering' function at Snap and Captions th...  View Skill → →

AI Transformation Partner

Start Your Journey

SERVICES  AI Audit AI Automation AI Training    COMPANY  About Case Studies Book a Call

© 2026 Refound. All rights reserved.