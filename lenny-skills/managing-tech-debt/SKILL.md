# Managing Tech Debt

**Category:** Engineering

**Source:** https://refoundai.com/lenny-skills/s/managing-tech-debt

---

Managing Tech Debt | Refound AI

Lenny Skills Database     SKILLS  PLAYBOOKS  GUESTS  ABOUT               SKILLS  PLAYBOOKS  GUESTS  ABOUT                     Engineering   18 guests | 20 insights

Managing Tech Debt  Technical debt is a strategic tool, not just an engineering burden. Startups should deliberately take on debt to move faster, while mature companies must pay it down to avoid grinding to a halt. The key is understanding when debt is serving you versus when it's blocking innovation.

Download Claude Skill

Read Guide

The Guide  5 key steps synthesized from 18 experts.

1 Treat tech debt as strategic leverage  At early stages, technical debt is how you outpace larger competitors. Deliberately defer problems that a future hire can solve. The goal is to buy speed now in exchange for cleanup later. Tech debt is a 'champagne problem' that means people are actually using your product.

Featured guest perspectives

"I actually think as a startup your job is to take on technical debt because that is how you operate faster than a bigger company."

— Gaurav Misra    "I try to remind the engineers, we would be so lucky to have tech debt because that means people are using the product... what we didn't need at launch was a distributed scheduler with coworkers and RabbitMQ. We just didn't need it because we had no users."

— Julia Schottenstein        2 Monitor your 'debt interest rate'  Watch for the inflection point when debt stops serving you. If maintenance takes up 80-90% of engineering time, you've run out of technical debt runway. Systematic slowness is often a symptom of accumulated debt that requires pausing feature work to fix foundational issues.

Featured guest perspectives

"Monitor the 'interest' paid on debt - if maintenance takes up 80-90% of time, you have run out of technical debt runway."

— Gaurav Misra    "You always have to keep in mind tech debt and there might be, when you're moving slow, systematic reasons for that. How do you make sure that you're not grinding to a halt because things are built the wrong way?"

— Dylan Field        3 Avoid the 'big bang' rewrite trap  Engineers chronically underestimate migration time for system rewrites, and you must support the old system while building the new one. Instead of full rewrites, incrementally uplift specific APIs or components. Take pieces of the old system and make them more scalable rather than starting from scratch.

Featured guest perspectives

"Engineers notoriously, notoriously, notoriously, massively underestimate the migration time for old system to new system and that causes a lot of problems. By the way, you still have to support the old system while you're working on the new system."

— Camille Fournier    "The decision that was done... they needed to do a complete rewrite in order to get there. This is a decision that never works out for anyone... We try to bring the site up and just keeps crashing. And so it basically takes us a month to get it fully functional again."

— Will Larson        4 Make deleting code a priority  Small teams must prioritize code deletion over addition to avoid unsustainable maintenance burden. Engineers naturally add incremental features that carry hidden long-term costs. Create explicit incentives like a 'Delete Code Club' to regularly audit and remove unused code.

Featured guest perspectives

"Deleting code is more important than writing it a lot of the time... engineers have a tendency to add these little incremental wins that actually add more of a long-term maintenance cost than is clear."

— Keith Coleman & Jay Baxter    "We have a Delete Code Club. We can always almost find a million-plus lines of code to delete, which is insane. ... Everything gets easier, right? Codelets loads faster. It's easier to understand."

— Farhan Thawar        5 Own tech debt as a product problem  Technical debt should be viewed as 'product debt' that PMs own alongside engineers. Include infrastructure stability in your top priorities. You can't build a skyscraper on a shaky foundation, so treat foundational stability as a prerequisite for new features.

Featured guest perspectives

"Infrastructure is the product. Period. People are like, 'Oh, tech debt.' I'm like, 'Yeah, it's a product debt.' I cannot build a skyscraper on a shaky foundation. So it is your problem too."

— Ebi Atawodi    "Sometimes teams are just getting bogged down by really urgent work. There's too much tech debt. There's too much product debt. Bugs, instability... There's just no way that they're going to be able to focus on the enlightened, bigger, creative stuff if they're just heads-down dealing with incidents all day."

— Eeke de Milliano

✗ Common Mistakes

Attempting a 'big bang' rewrite instead of incremental improvementUnderestimating migration time and the burden of supporting two systems simultaneouslyOver-engineering at launch before demand is provenLetting debt accumulate until teams spend 80%+ of time on maintenanceTreating tech debt as 'engineering's problem' rather than a shared product concern     ✓ Signs You're Doing It Well

Engineering time spent on maintenance stays under 20-30% consistentlyTeams can ship new features without constantly fighting infrastructure firesCode deletion happens regularly and is celebrated, not just code additionDebt is taken on deliberately with a clear payback plan, not accidentally

All Guest Perspectives

Deep dive into what all 18 guests shared about managing tech debt.

Adriel Frederick 1 quote

Listen to episode →

"The answer was like, Yo, we got to rebuild it. There was no answer where we couldn't have a product like this. We needed some ability to be able to influence prices so that we could actually run an effective marketplace. The current solution didn't work. It wasn't as operationally flexible as we needed it to be."  Tactical:  Evaluate if current technical debt is preventing necessary operational control.Be willing to admit when a complex algorithmic approach has failed and pivot to a more flexible architecture.

View all skills from Adriel Frederick →

Austin Hay 1 quote

Listen to episode →

"The job of a marketing technologist is to think often one to two years down the road about what we're going to need to solve for and design systems in an elegant way, not to break the bank, but to at least be the minimum viable product to actually get there. And a lot of my job, and I think the job of marketing technologists is trying to preserve that future state in the most minimally invasive engineering and resource way possible."  Tactical:  When setting up tools, ask: 'What happens a year from now if I don't change anything?'Implement foundational elements like SSO or proper data schemas early to avoid catastrophic migrations later.

View all skills from Austin Hay →

Camille Fournier 2 quotes

Listen to episode →

"Engineers notoriously, notoriously, notoriously, massively underestimate the migration time for old system to new system and that causes a lot of problems. By the way, you still have to support the old system while you're working on the new system."  Tactical:  Account for significant migration time when planning system updatesPlan for the resource cost of supporting the legacy system during a transition    "Take pieces potentially of the old system, uplift them, make them more scalable, make them easier to work with, clean up the tech debt, but trying to say we're going to just go away. We're going to rewrite, we're going to build something brand new and it's going to solve all our problems, it just very rarely works."  Tactical:  Uplift specific APIs or components rather than the whole frameworkCreate a staged plan for system evolution

View all skills from Camille Fournier →

Casey Winters 1 quote

Listen to episode →

"The idea is that some of the most impactful projects that product teams can work on at scale... are the hardest to measure. And because of that, they just get chronically underfunded... I walk through some examples of a few tactics that work to get around this problem, building custom metrics to show the value, being able to run small tests that prove the worthwhile-ness of the investment."  Tactical:  Build custom metrics to demonstrate the business value of performance or stabilityRun small tests to prove that technical investments will yield long-term resultsAlign with engineering and design peers to present a unified front for technical investments

View all skills from Casey Winters →

Dylan Field 1 quote

Listen to episode →

"You always have to keep in mind tech debt and there might be, when you're moving slow, systematic reasons for that. How do you make sure that you're not grinding to a halt because things are built the wrong way or you rush to get something out, and you need to go and fix the underlying infrastructure or way that you built it in some form?"  Tactical:  Investigate systematic reasons for slow development paceBalance infrastructure fixes with feature development to maintain long-term speed

View all skills from Dylan Field →

Eeke de Milliano 1 quote

Listen to episode →

"Sometimes teams are just getting bogged down by really urgent work. There's too much tech debt. There's too much product debt. Bugs, instability... There's just no way that they're going to be able to focus on the enlightened, bigger, creative stuff if they're just heads-down dealing with incidents all day."  Tactical:  Diagnose when a team is stuck in a 'hierarchy of needs' trap due to instabilityPrioritize debt reduction to free up headspace for creative work

View all skills from Eeke de Milliano →

Gaurav Misra 1 quote

Listen to episode →

"I actually think as a startup your job is to take on technical debt because that is how you operate faster than a bigger company."  Tactical:  Evaluate if a problem can be solved by a future hire (e.g., the 500th engineer) rather than solving it today.Monitor the 'interest' paid on debt—if maintenance takes up 80-90% of time, you have run out of technical debt runway.Dedicate specific periods (like Q4) to paying down accumulated debt when product cycles slow down.

View all skills from Gaurav Misra →

Geoff Charles 1 quote

Listen to episode →

"We don't have a bug backlog. We fix every bug once they're surfaced almost."  Tactical:  Assign bugs directly to the engineer on call to ensure immediate pain awareness.Use a rotational production engineering program to protect core teams from escalations.

View all skills from Geoff Charles →

Julia Schottenstein 1 quote

Listen to episode →

"I try to remind the engineers, we would be so lucky to have tech debt because that means people are using the product... what we didn't need at launch was a distributed scheduler with coworkers and RabbitMQ. We just didn't need it because we had no users."  Tactical:  Build the simplest, most 'naive' version of a feature first (e.g., a simple for-loop) to validate demand.Accept technical debt as a trade-off for getting the product into users' hands faster.

View all skills from Julia Schottenstein →

Keith Coleman & Jay Baxter 1 quote      "deleting code is more important than writing it a lot of the time... engineers have a tendency to add these little incremental wins that actually add more of a long-term maintenance cost than is clear... you get forced to do this, by the way, when you have such a small team."  Tactical:  Audit systems regularly to delete 'incremental wins' that have high long-term maintenance costsAggressively remove 'cruft' to keep the core system manageable by a small number of people

View all skills from Keith Coleman & Jay Baxter →

Maggie Crowley 1 quote

Listen to episode →

"Where are your technical hurdles? What are the big pieces of tech debt? What are your engineering and technical teams always harping on that they want to invest in?"  Tactical:  Interview engineering teams to identify critical technical hurdlesInclude technical debt investments as a core part of the product strategy

View all skills from Maggie Crowley →

Matt Mullenweg 2 quotes

Listen to episode →

"Well, that's why I think technical debt is one of the most interesting concepts. There's so many companies as well that maybe have big market caps, but I feel like they might have billions or tens of billions of dollars of technical debt. You can see in the interface or how their products integrate with themselves through things."  Tactical:  Identify technical debt by looking for inconsistencies in the user interface and product silos    "And it's a big focus for us this year, is actually kind of going back to basics, back to core, and improving all of those kind of nooks and crannies of the user experience, and also ruthlessly editing and cutting as much as possible, because we just launched a lot of stuff over the past 21 years that maybe is not as relevant today or it doesn't need to be there."  Tactical:  Perform a 'back to basics' audit to identify and remove features that no longer serve the primary user goalFocus on the 'nooks and crannies' of the UX to resolve accumulated friction

View all skills from Matt Mullenweg →

Melanie Perkins 1 quote

Listen to episode →

"We were doing a front-end rewrite and we thought it would take about six months... and then it took two years and it was two years of not shipping any product, two years of a product company not being able to ship product."  Tactical:  Gamify long-term technical projects (e.g., using a game board with rubber ducks) to maintain team momentum during 'dark' periodsAccept that foundational rewrites are necessary to enable future features like cross-platform collaboration

View all skills from Melanie Perkins →

Tomer Cohen 1 quote

Listen to episode →

"We have the maintenance agent when you have a failed build, it will do it for you. In fact, I think we're close to 50% of all those builds being done by the maintenance agent and a QA agent."  Tactical:  Deploy 'Maintenance Agents' to automatically resolve failed software buildsUse AI agents to pick up and fix bugs directly from Jira tickets

View all skills from Tomer Cohen →

Upasna Gautam 1 quote

Listen to episode →

"One sprint might be high-priority feature development, in another sprint maybe we're focused on medium-priority optimizations and bug fixes. But we know that any time there's a critical incident in production, it also takes critical priority over everything else."  Tactical:  Establish a clear escalation protocol for critical incidents to protect the team's focusRotate sprint focus between new features and optimizations based on current platform health

View all skills from Upasna Gautam →

Ebi Atawodi 1 quote

Listen to episode →

"infrastructure is the product. Period. People are like, 'Oh, tech debt.' I'm like, 'Yeah, it's a product debt.' I cannot build a skyscraper on a shaky foundation. So it is your problem too. It's not for the engineer to be barging on the door and be like, 'Oh, there's a problem.'"  Tactical:  Include infrastructure and tech debt in your 'Top 10 Problems' listTreat foundational stability as a prerequisite for building new features

View all skills from Ebi Atawodi →

Farhan Thawar 1 quote

Listen to episode →

"We have a Delete Code Club. We can always almost find a million-plus lines of code to delete, which is insane. ... Everything gets easier, right? Codelets loads faster. It's easier to understand."  Tactical:  Create a 'Delete Code Club' or dedicated hack day teams focused solely on removing codeProvide a manual or guide for engineers on how to identify and safely delete unused code

View all skills from Farhan Thawar →

Will Larson 1 quote

Listen to episode →

"The decision that was done... they needed to do a complete rewrite in order to get there. This is a decision that never works out for anyone... We try to bring the site up and just keeps crashing. And so it basically takes us a month to get it fully functional again."  Tactical:  Be wary of 'death march' rewrites intended to solve social or architectural problemsExpect significant debugging periods (e.g., 30 days) when launching major architectural shifts

View all skills from Will Larson →

Install This Skill

Add this skill to Claude Code, Cursor, or any AI coding assistant that supports Agent Skills.

1  Download the skill

Download SKILL.md

2  Add to your project

Create a folder in your project root and add the skill file:

.claude/skills/managing-tech-debt/SKILL.md    3  Start using it

Claude will automatically detect and use the skill when relevant. You can also invoke it directly:

Help me with managing tech debt              Related Skills Other Engineering skills you might find useful.    19 guests    Engineering Culture A high-performance engineering culture can be built around extreme experimentation frequency and tig...  View Skill → →      5 guests    Platform & Infrastructure The success of major platforms (like WhatsApp or Instacart) often depends on 'invisible' infrastruct...  View Skill → →      1 guests    Technical Roadmaps A written strategy is essential for organizational alignment and provides a baseline that can be cri...  View Skill → →      2 guests    Design Engineering The guest discusses the creation of a specific 'Design Engineering' function at Snap and Captions th...  View Skill → →

AI Transformation Partner

Start Your Journey

SERVICES  AI Audit AI Automation AI Training    COMPANY  About Case Studies Book a Call

© 2026 Refound. All rights reserved.