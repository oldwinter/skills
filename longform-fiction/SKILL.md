---
name: longform-fiction
description: Long-form fiction manuscript workflow that plans, drafts, or expands a novel, novella, or serial with a story bible, per-chapter contracts, parallel or sequential chapter workers, continuity checks, and word/character-count acceptance gates. Use when asked to write, draft, expand, or continue a manuscript at chapter scale (about 10k+ words), turn a premise or existing draft into chapters, fix continuity across chapters, or hit a target length such as 60k Chinese characters; not for articles, blog posts, marketing copy, translation, or single-scene brainstorming.
---

# Longform Fiction

You are the showrunner. You own canon, contracts, gates, and the delivery; chapter workers only write prose. Nothing gets drafted before the story bible and chapter plan exist.

## Route the request

- New manuscript from a premise, outline, or setting: work through steps 1-8.
- Existing draft to expand, continue, or finish: step 1 first, then steps 2-8. The draft is canon evidence, not disposable text.
- Continuity or consistency repair only: step 1, then step 6, then the final report.
- Single scene, single chapter idea, or outline only: this skill is not needed; produce the outline and stop.

## 1. Read the material and establish canon

Read every supplied source in full (existing draft, notes, setting research, prior bible). Index it before judging it: path, chapter or section, what it establishes, what it leaves unresolved. Separate three registers, and keep them separate for the rest of the task:

- **canon**: established facts that must not change (names, dates, ages, injuries, places, promises);
- **draft**: text that may change, but only with approval and a backup;
- **intent**: what the user says they want, which outranks your interpretation.

Do not summarize away continuity facts while reading.

Completion criterion: every source has an index entry; canon candidates and contradictions are listed; no new prose has been written yet.

## 2. Confirm the writing contract

Resolve and write down every row below. Ask one batch of questions only for rows that would change the manuscript; infer the rest from sources and the conversation. If the user says to just go, fill the defaults and record them.

```text
Language:        <e.g. Chinese, simplified>
Genre:           <e.g. historical mystery>
Target length:   <number> <unit: words or characters, tolerance>
Chapters:        <count, average length, or volume/act structure>
POV / tense:     <e.g. third past, two alternating leads>
Audience/limits: <rating, content constraints, style models>
Delivery:        <manuscript path(s) and format, bible path>
```

The length unit must be explicit because "60k" means words in English and characters in Chinese. Pick the unit from the user's own wording, then use it everywhere, including in step 7.

Completion criterion: every row has a value; the length unit and tolerance are explicit; the user approved the table or said to proceed.

## 3. Write the story bible

`bible.md` next to the manuscript. Keep it terse and structured, one row or one block per fact:

- premise and logline;
- characters: name, aliases, role, want, fear, arc, speech register, first appearance;
- world rules and constraints that later chapters depend on;
- timeline: dated or ordered events with sources;
- open threads: every promise or question, its setup, planned payoff chapter, or "unresolved by design";
- terminology: places, institutions, invented terms, and their exact spelling.

Completion criterion: every entity that appears in the chapter plan is in the bible; every open thread has a payoff chapter or an explicit unresolved-by-design note; every name this plan relies on has one spelling.

## 4. Write chapter contracts

One contract per chapter, in `chapter-contracts.md` or in the plan file. Fields:

```text
Chapter N: <working title>
POV / tense: <who, which tense>
Goal:        <what changes by the end>
Beats:       <3-7 ordered beats>
Continuity:  <facts it must honor; facts it establishes for later chapters>
Ending:      <the state the next chapter starts from>
Target:      <count for this chapter>
```

Contracts are the workers' only source of truth. Do not add canon in a contract unless it is first recorded in the bible.

Completion criterion: every planned chapter has a contract; chapter targets sum to the total within 2 percent; each contract's continuity-in and continuity-out lines are filled.

🔴 CHECKPOINT — PLAN APPROVAL: present the contract table, one-paragraph premise, cast list, and chapter table to the user; draft only after approval or an explicit go-ahead. A plan rejected here saves the most rework. If the user already said to go, continue without asking again.

## 5. Draft chapters

Choose the execution mode from what the harness actually provides:

- **Parallel workers** when the harness exposes subagents or task tooling: one worker per chapter, started in small batches (2-4 to begin) and grouped by adjacent chapters so continuity context is fresh. Start with the first batch and verify it before launching the rest.
- **Sequential** when no such tooling exists: draft in chapter order. Say so in the report. Never claim or simulate parallelism.

Every worker gets the same packet, always: `bible.md`, its own chapter contract, 8-12 line summaries of the previous and next chapters (or the nearest written ones), a short voice sample, and these hard rules:

- write only the contracted chapter, POV, tense, and ending state;
- use only canon names and facts from the bible; mark genuinely new minor details `[new]` in a return note, and never invent named characters or plot facts that canon depends on;
- no headings the contract does not ask for, no recap of earlier chapters, no meta commentary about the process;
- hit the contract target within tolerance; return the chapter text plus a 5-line summary and any `[new]` notes for the merge pass.

If a worker fails, times out, or returns a stub: retry once with the same packet and a stricter format reminder. Second failure: draft that chapter yourself sequentially, log the failure, and continue. Do not wait indefinitely and do not accept a fake chapter.

Completion criterion: every planned chapter exists at its planned path, its beats appear in order, and its count is within 15 percent of target. Chapters that miss this are fixed in step 6, not silently accepted.

## 6. Continuity merge

Read all chapter artifacts and build one conflict table across the manuscript:

| Fact class | Cases checked |
|---|---|
| Names and aliases | spelling, titles, who knows whom |
| Dates, ages, durations | timeline order, travel and recovery time |
| Places and geography | distances, rooms, who is where |
| Physical facts | injuries, objects, weather, clothing |
| Repeated/missing info | recap repeats, setups with no payoff |
| Voice | POV slips, tense slips, speech register drift |

Resolve in priority order: hard contradiction, then timeline, then naming, then repeated information, then voice. Every accepted change is recorded in the bible with the chapter and reason. When a fix requires editing a later chapter, make that edit in the same pass or mark the conflict open.

Completion criterion: the conflict table is complete and every row is fixed or marked open; the bible records every accepted change; no contradiction that a later chapter depends on is left unmarked.

## 7. Count gate

Measure every chapter and the total with one consistent unit and counting rule. Use [scripts/count_words.py](scripts/count_words.py) when the unit is characters or mixed Chinese/English text (`python3 <this skill's folder>/scripts/count_words.py <manuscript-dir>`; count = CJK ideographs + Latin word tokens), or the user's counting tool when they name one. Report per chapter and total, with the delta against the contract.

- Under target but within tolerance: leave it.
- Under by more than 15 percent: expand texture, dialogue, and description inside existing contracts before adding chapters; if still short, propose new scenes or chapters as a plan and ask.
- Over by more than 15 percent: cut redundancy and repeated information first; propose structural cuts before deleting plot; ask before removing more than 10 percent of existing prose.

Never pad with filler sentences, repeated reflection, or recap to reach a number.

Completion criterion: per-chapter and total counts are measured and reported; tolerance or an approval is recorded; no count is claimed without a measured number.

## 8. Assemble and deliver

Assemble in chapter order into the agreed delivery: one manuscript file, or one file per chapter in a directory. Keep the agreed format (Markdown is the default). If another document format is requested, convert with the harness's document tool after the Markdown is final. Do not add a title page, front matter, or metadata the user did not ask for.

Completion criterion: manuscript file(s) exist and open; chapter order matches the plan; the count table matches the delivered files; no placeholders, TODOs, or missing chapters remain.

## Final report

Return this contract, filled with measured values:

```text
Manuscript: <path(s), format, chapter count>
Bible:      <path>, <N> canon updates recorded
Counts:     target <X> <unit>; actual <Y> (<delta>); per-chapter table attached
Continuity: <N> fixed, <M> open: <one line each>
Workers:    <parallel or sequential; failures and retries>
Next:       <actions the user may want>
```

## Failure modes

| Trigger | First fix | Fallback |
|---|---|---|
| A worker fails, hangs, or returns an empty/stub chapter | Retry once with the same packet and a stricter output format | Draft that chapter sequentially yourself, log the failure, list it in the report |
| The harness has no subagent or task tooling | Draft sequentially in chapter order and say so | If the context cannot hold the plan, split by act and keep bible plus summaries in context |
| The context window cannot hold the whole manuscript | Keep the bible, contracts, and summaries in context; read chapters only for merge | Split the manuscript by act or chapter range, write a progress table, and resume from it |
| Two chapters contradict each other | Resolve from the bible/timeline and pick the canonical value | If canon is unclear, fix the earlier chapter, update the bible, mark the conflict open and flag it |
| Total length is under target | Expand existing scenes and beats inside their contracts | Propose added scenes or chapters as a plan and ask |
| Total length is over target | Trim redundancy, repeated information, and filler description | Propose structural cuts before deleting plot; ask before cutting more than 10 percent |
| The user's existing draft could be damaged | Copy it to a backup path first and edit the copy | Never rewrite or delete in place; show the diff summary and ask |
| Counting unit or a needed source is missing | Ask once, listing the exact gap and the default you would use | Use this skill's documented count rule and state it; mark source gaps as open threads |
| A worker invents canon or new named characters | Quarantine that chapter's inventions, merge only what the bible supports | Record accepted additions in the bible, rewrite unsupported ones in step 6 |
| Requested document format cannot be produced | Deliver Markdown and say why the conversion failed | Never claim a converted file exists without opening it |

## Checkpoints

- 🔴 BEFORE DRAFTING: bible plus chapter plan approved (step 4).
- 🔴 BEFORE LARGE REWRITES: resequencing, POV/tense change, retcon, or cutting more than 10 percent — confirm scope and backup first.
- 🔴 BEFORE DISCARDING EXISTING PROSE: backup the file and get explicit approval; the user's draft wins over your plan.

## Do not

- Copy source texts verbatim; paraphrase and keep quoted material short and attributable.
- Change canon silently; every accepted change goes into the bible with chapter and reason.
- Rewrite or delete the author's existing draft without approval and a backup.
- Invent quotes, citations, sources, or real-world facts presented as sourced.
- Generate walls of prose without a contract and the count gate.
- Pad to hit a number with filler, repeated reflection, or recap.
- Put personal data, private material, or credentials in the bible, manuscript, or report.
- Add meta commentary, progress notes, or AI disclaimers inside the manuscript text.
- Claim a count, a chapter, or a deliverable that has not been measured or opened.

## Resources

- [scripts/count_words.py](scripts/count_words.py) — dependency-free counter for CJK characters plus Latin words. Read it only when step 7 needs a measured count, and pass the manuscript directory or files. `python3` may be `python` or `py -3` on Windows.
