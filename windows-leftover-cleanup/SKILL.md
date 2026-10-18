---
name: windows-leftover-cleanup
description: "Clean Windows leftovers from software that was removed or from a drive that no longer exists: Apps and features records, Steam library config, firewall rules, service registrations, file associations, app-state caches, and empty install directories. Use when uninstalled apps or games are still listed, when a drive such as D: disappeared, or when the user asks to clean registry leftovers (注册表残留)."
---

# Windows Leftover Cleanup

A leftover is a **record** whose owner is gone. The job is not "delete everything that mentions the old path": it is proving, record by record, that the owner is dead, then deleting exactly those records. Two terms carry the skill. A **dead root** is an install root that no longer exists — a removed drive, a deleted folder. A **record** is anything still pointing at one: a registry value, a config line, a firewall rule, a service entry, a directory.

## Trigger

Use this skill when:

- apps or games are gone from disk, yet Settings → Apps, a vendor launcher, or Steam still lists them;
- a drive or partition no longer exists after a disk change, and software records still point into it;
- an uninstall left firewall rules, service registrations, file associations, startup entries, or install directories behind;
- the user asks to clean 注册表残留, leftover registry entries, or says the registry was never cleaned.

A moved or upgraded install with a live owner is not a leftover: re-point it, or leave it.

## Ground rules

- **Dead root, live owner.** Delete a record only when its target is dead *and* the owning app is not installed elsewhere — another drive, another Steam library, another user profile. A dead path with a live app is a config to repair, not a record to delete.
- **OS-internal records stay.** Component Based Servicing, `Installer\Products` source paths, `EventLog` message files, `DriverDatabase`, and `Appx\PackageVolumes` point at install media and servicing state. Deleting them cleans nothing and damages Windows.
- **Restore point before every batch.** Export what you are about to touch, and hand the user the import commands. No restore path, no deletion.

## Workflow

1. **Prove the dead roots.** List volumes and drives, test the paths the software believes in, and read the software's own install or library config rather than assuming the registry is complete. Steam, for example, keeps its roots in the Steam client config as well as the game library.
   Completion criterion: every path root on the suspect list is marked dead or live, and each dead root is named explicitly.

2. **Take the restore point.** Export the registry keys, copy the config files, export the firewall policy, and write a short restore note beside the backup with the exact import commands.
   Completion criterion: every backup file exists and is non-empty, and the restore commands are written down and point at those files.

3. **Collect records in three passes.** First the product records — uninstall entries in both machine views and the user view. Then the app-state records — per-app flags, path-keyed caches, shell and GameDVR caches. Then a raw reference scan for each dead root across the user and machine hives. Classify every hit as delete, repair, or keep, with the reason recorded.
   Completion criterion: the list holds no unclassified hit, and every keep names its owner (live app or OS-internal).

4. **Delete in least-privilege order.** Delete user-hive records in the current process. Delete machine-hive records, services, and `Program Files` directories through one elevated child process, and read every operation's exit status back. Prefer direct registry or API calls over `reg.exe` when key names contain backslashes, CJK, or trailing spaces.
   Completion criterion: every targeted record re-reads as absent, and every failure has a named cause and a decision.

5. **Re-scan to zero.** Run the same collection scan again. The expected end state is zero app-owned hits; OS-internal hits are expected, listed in the report, and left alone.
   Completion criterion: the re-scan reports zero records whose owner is a removed app or a dead root.

6. **Report and hand back.** Report what was deleted by area with counts, what was kept and why, the backup path, the restore commands, and any record that still needs the user's decision.
   Completion criterion: the report lets the user verify and undo every change without re-reading the conversation.

## Scan mechanics that decide success

- Search whole hives directly. `reg query <key> /f "D:\" /s /d` is a substring match, so anchor on the root (`D:\SteamLibrary`) and judge each value. In PowerShell backslashes are literal: `"D:\\"` searches for two backslashes and finds nothing.
- Walk hives with a recursive .NET key scan when you need the value's full path and kind. Some records are `REG_BINARY` keyed by path (Compatibility Assistant); others use the path as the value *name* (MuiCache, FeatureUsage). A string-only scan misses the binary ones.
- Check both registry views. `HKLM\SOFTWARE\...` and its `WOW6432Node` mirror answer separately; a key deleted in one view still answers from the other.
- Windows PowerShell 5.1 reads `.ps1` files as ANSI, so a script holding CJK key names mangles them on the way into an elevated child process. Pass such scripts as `-EncodedCommand` (UTF-16LE base64).
- Elevation: `Start-Process -Verb RunAs` prompts by default. With `ConsentPromptBehaviorAdmin` at 0 on an admin account it elevates silently; otherwise ask the user to approve the UAC dialog instead of assuming the work ran.
- Hunt the second copy of live config. Steam writes library roots to both `steamapps\libraryfolders.vdf` and `config\libraryfolders.vdf`; cleaning one leaves Steam finding the dead root again.
- MSI products: uninstall with `msiexec /X{GUID} /qn`, which removes the `Uninstall` key and the `Installer\UserData\...\Products` registration together. Delete an orphan `Uninstall` key only after the product registration and the install directory are both gone.

## Delete or keep

| Record | Delete when | Otherwise |
| --- | --- | --- |
| Uninstall entry | target dead and app not installed elsewhere | leave; it belongs to a live install |
| Steam app state or library entry | game absent from every library manifest | leave entries for installed games |
| Firewall rule | its program path sits under a dead root | leave live-app rules and report them |
| Service or driver entry | binary missing and service stopped | leave; a live service is not a leftover |
| File association or protocol handler | handler binary sits under a dead root | leave when the app exists on another path |
| App-state cache (MuiCache, FeatureUsage, GameDVR, tray icons) | keyed by a dead path | leave live-app records |
| Empty install directory | zero files recursively | leave directories that hold files |
| OS-internal servicing record | never | leave it and say why in the report |

Per-area enumeration commands, the exclusion list, and the restore recipe live in [references/registry-sweep.md](references/registry-sweep.md).
