# Scoped Windows cleanup

## Freeze the batch

Persist the exact absolute paths, owning application, type, size, timestamp, expected effect, authorization basis, and protected paths. Add file identity or a digest where replacing a reviewed file would change the decision. Keep the manifest separate from its execution receipt. Inspect resolved targets and every ancestor for junction/reparse redirection before deleting.

Prefer the owning package manager or uninstaller when it maintains an index. For reviewed diagnostic files and completed downloaded installers, use explicit files with `Remove-Item -LiteralPath`; retain unrelated files and the owner directory. Avoid broad recursive deletion. If recursion is genuinely required, validate the resolved absolute boundary and all link entries first, use one shell end to end, and verify the result.

Immediately before execution:

1. Refresh free space and metadata. Exclude missing or changed files and record why.
2. Check running programs and installer/updater processes by their executable paths. A newer main executable running elsewhere does not prove an older installation is abandoned; a staged update may still own it.
3. Confirm install completion when removing an installer. Compare the installed version with the download; preserve current staged updates and rollback data unless included in scope.
4. Skip locked files. Do not kill the owner or reboot merely to improve the cleanup total. If quitting the app is necessary and authorized, let it exit normally and recheck.
5. Apply only the reviewed scope. Existing user authorization persists; ask only if scope or consequences have changed.

Age is supporting evidence, not proof. A recently modified Temp directory can contain both finished installers and active work. File deletion can succeed even while another process uses the file with delete sharing, so lock probing alone does not replace owner/process checks.

## Owner-specific decisions

| Owner / data | Action and consequence |
|---|---|
| npm, uv, pnpm, Go, Scoop caches | Prefer the tool's cache command after checking current CLI help; account for hardlinks and active installs. Rebuilds or downloads may follow. |
| Browser / Electron cache | Use the app's cache entry point or an exact cache subtree after exit. Cookies, IndexedDB, session restore, local storage and site offline data have different consequences. |
| Game logs | Remove only reviewed stale diagnostic logs while the game is closed; retain configuration, saves and resources. |
| Model downloads / Playwright browsers | Confirm whether offline inference or automation still needs them; show reinstall cost and owner. |
| Duplicate app installs | Match process paths, version, install registration, pending updates and user-data paths before choosing an uninstaller. |
| Repository / worktree | Inspect status, branches, unpushed commits, remotes, worktree ownership and special data before considering removal. “Prunable” is not permission. |
| Agent data | Preserve conversation history, memory, databases and active tool runtimes. A directory named `.cache` may still hold required models or profiles. |
| WSL / Docker virtual disk | Compare guest used space, host allocation and logical length. Use the product's supported trim/compact procedure, including its shutdown requirements, only when authorized. |

Validate duplicates by content where worthwhile, but distinguish duplicate content from interchangeable ownership. Separate applications may need their own identical DLL. Do not unlink one because another copy exists.

## Windows-managed storage

After `DISM /AnalyzeComponentStore`, ordinary authorized cleanup can use:

```powershell
dism.exe /Online /Cleanup-Image /StartComponentCleanup /English /NoRestart
```

Read the current [Microsoft cleanup documentation](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/clean-up-the-winsxs-folder) before execution. This removes superseded components immediately rather than waiting for the scheduled task's grace period. Run only one servicing job, record its exit code, and analyze the component store again after it completes. Skip while another servicing operation or an unresolved reboot requirement makes the state uncertain.

`/ResetBase` additionally removes the ability to uninstall existing update packages. It is a separate consequential decision, not a default cleanup flag. Never delete WinSxS or Windows Installer files by hand. [Windows Installer cache](https://learn.microsoft.com/en-us/troubleshoot/windows-client/application-management/missing-windows-installer-cache) supports repair, update and uninstall operations.

Shadow copies are recovery data. VSS allocated, used and maximum values are different. Deleting restore points or shrinking the quota can remove recovery history and requires authorization for that consequence. A pagefile with real usage is not idle space; retain it unless a separate memory-sizing decision justifies a change. Check whether hiberfil.sys exists before predicting a hibernation saving.

## Receipt and verification

For each path or owner command, record attempted action, outcome, exit code/error, expected bytes and observed remaining state. A successful process launch is not a successful cleanup; poll its completion and read the output. For a system operation, native command exit codes must be captured immediately.

Measure volume free space before and after the batch, then refresh the affected subtrees. Report both the removed-file estimate and net volume change. Do not run system cleanup and user-cache deletion concurrently if you need attributable savings. Restore snapshots and other applications can consume newly freed space.

Verify protected data remains, retain failed/skipped items for a later handoff, and preserve the original target baseline across refreshed scans. When another session also cleans the disk, report that separately rather than claiming its result.
