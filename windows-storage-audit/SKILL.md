---
name: windows-storage-audit
description: Scan Windows disks from their roots, explain physical storage use and cleanup feasibility, then execute scoped cleanup with before/after evidence when authorized. Use for deep disk audits, storage reduction targets, caches, installers, or protected system space.
---

# Windows storage audit and cleanup

Use Windows APIs and native PowerShell. Produce a measured space budget, concrete cleanup candidates, and evidence of any authorized changes. Preserve the user's retained apps, games, documents, development state, and recovery requirements across turns.

## Establish the scope

- Inventory physical disks and volumes before picking roots. A removable boot drive can expose several letters; an old registry install path can now point to an unrelated volume. Use live files and volume identity as evidence.
- Record used/free bytes and time before scanning. Freeze any reduction target against that baseline. Use GiB consistently, or label decimal GB explicitly.
- Compare retained data with the target early. If protected content alone exceeds the desired final occupancy, explain that constraint; offer a revised target, supported resource reduction, or migration without treating those alternatives as authorized.
- Put machine-specific paths, reports, manifests, and receipts in a private task output directory. Keep the installed skill free of device inventories and private runtime data.

## Scan

Read [measurement.md](references/measurement.md) for native inventory commands, Python discovery on Windows, and administrator supplementation.

Run the bundled scanner with explicit roots and a **new** output directory:

```powershell
& $auditPython "$skillRoot\scripts\scan_storage.py" --root C:\ --output "$auditRoot\scan-01"
```

The scanner reads file metadata, accounts for allocation and hardlinks, and records inaccessible paths and skipped links. Use its `--help` for current options and output schema. Partial scans remain useful evidence but are not complete scans; report their exit status and coverage.

Analyze root totals, then drill into the largest owners. Keep logical bytes, physical allocation, and expected reclaim separate. Directory hardlink attribution depends on traversal order; removing one cache entry may free nothing while another link exists. Do not add parent and child totals or count a duplicate-installer finding again on top of its containing cache.

Use system APIs for shadow storage, component-store size, and filesystem metadata when the file totals leave a material gap. A non-elevated account named Administrator is still non-elevated. If authorized elevation is available, run only the scoped helper through normal UAC; record errors otherwise. An elevated scan can still have unreadable directories. Do not change ACLs or take ownership to make an audit look complete.

Recheck volume usage and selected candidates before deciding. If another session or application changes occupancy materially, identify the change and create a fresh snapshot. Attribute another session's cleanup separately from this run.

## Classify and clean

Read [cleanup.md](references/cleanup.md) before any mutation. Reuse authorization already granted for the same objects and scope; a scan request alone does not authorize deletion. Finish a reviewable manifest before requesting any genuinely missing authorization.

Classify candidates by owner and consequence, not directory names:

| Candidate | Decision |
|---|---|
| Cache, completed installer, old diagnostic log | Confirm the owner and active work; retain current update files |
| Installed program, local model, browser runtime, site offline data | Explain lost capability and replacement cost before including it |
| Repository, worktree, local database, conversation history | Check ownership and unsynced work; preserve until specifically included |
| Windows component store, restore points, pagefile, installer database | Use the specific Windows procedure; never treat the containing directory as disposable |

Respect the retained-game constraint. Game resource packages are not duplicate junk because their names or sizes resemble each other. A launcher's supported resource manager may remove optional content, but count only the amount it reports for the user's chosen configuration.

## Finish

Report the initial baseline, current occupancy, actual net change, what this run changed, remaining candidates, and the unresolved gap. Separate estimated file bytes removed from observed free-space gain; concurrent writes, hardlinks, and restore snapshots can make them differ.

For execution, require a receipt with completed, skipped, changed-since-review, and failed paths or commands. Confirm protected paths still exist and any owner-specific validation succeeded. A process launch is not completion. For scans, retain errors and links alongside the directory and large-file results.

Keep the final response focused on the achievable target, the largest opportunities, and clickable evidence. Do not claim a percentage reduction that the final volume measurement does not support.
