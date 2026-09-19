# Windows measurement

## Native inventory

These commands are read-only. Store output in a private, timestamped task directory.

The collector saves volume/media identity, pagefile usage and current-user AppX paths with per-query status. Use a new output directory; it refuses existing directories and redirected ancestors. Exit 2 means partial evidence.

```powershell
& "$skillRoot\scripts\collect_system_storage.ps1" -OutputDirectory "$auditRoot\system-01"
```

```powershell
Get-CimInstance Win32_DiskDrive |
    Select-Object Index,Model,MediaType,Size,InterfaceType
Get-CimInstance Win32_LogicalDisk |
    Select-Object DeviceID,DriveType,FileSystem,VolumeName,Size,FreeSpace
Get-Volume |
    Select-Object DriveLetter,DriveType,FileSystemType,Size,SizeRemaining,AllocationUnitSize
Get-ChildItem -LiteralPath 'C:\' -Force |
    Select-Object Name,Length,Attributes,LinkType,Target
Get-CimInstance Win32_PageFileUsage |
    Select-Object Name,AllocatedBaseSize,CurrentUsage,PeakUsage
```

`Get-PSDrive` supplies a quick volume check; CIM and Get-Volume establish media and filesystem identity. Do not infer today's device capacity from an uninstall registry entry's EstimatedSize. Use registry entries to identify owners, and verify their live install paths.

Validate an actual Python interpreter before scanning. The WindowsApps `python.exe` alias can return no usable interpreter. Prefer an existing virtual environment or `uv python find --no-python-downloads`, then run that interpreter's `--version`. The scanner requires Python 3.10+ and only the standard library. Do not install a new environment merely to scan when an existing interpreter works.

PowerShell 5.1 and 7 are both common. Read Chinese text using `Get-Content -Encoding UTF8`; set `PYTHONIOENCODING=utf-8` for Python output when needed. Use `-LiteralPath` and structured arguments for paths with spaces, brackets, Unicode, or `$`.

## Accounting

- **Volume used** is total minus free bytes. It is the outcome measurement.
- **Logical size** is file length. Sparse virtual disks and cloud placeholders can make it misleading.
- **Allocated size** is disk storage assigned to a file, with compression/sparsity handled by the Windows API. FileStandardInfo and GetCompressedFileSize serve different cases; plain uncompressed GetCompressedFileSize can return logical length rather than cluster-rounded storage.
- **Unique allocated size** deduplicates file identities. This prevents counting NTFS hardlinks repeatedly, notably WinSxS, package stores, and virtual environments.
- **Reclaimable space** depends on ownership, links outside the candidate, lock state, cleanup semantics, and replacement data. An early traversal's attribution to a cache is not proof that deleting that cache releases the bytes.

The scan intentionally excludes directory junctions and symbolic links. Record the skipped entries. A selected root or its ancestor must not redirect to another tree silently. Cloud placeholders must not be hydrated merely for size or duplicate checks. Hash only justified local duplicate candidates, preferably known installers, after filtering by size; do not hash a whole cloud-backed drive.

Count every candidate once. For a hardlinked candidate, compare links observed inside the candidate with the file's total link count; exclude bytes held by links outside it from a firm reclaim estimate. If identity or allocation cannot be read, expose unknown or estimated counts separately.

## Administrator supplementation

Use an already elevated shell, or normal user-visible UAC when the task authorizes the read-only helper. Keep the window hidden except for required UAC interaction. Save native command output and exit codes. Do not silently retry using scheduled tasks, services, ownership changes, or another identity.

In an elevated shell, the same collector with `-IncludeProtected` adds the queries below, flattens CIM volume references, and records native exit codes. It performs no automatic elevation, cleanup or ownership changes. A live servicing process defers the DISM analysis rather than starting another job.

```powershell
Get-CimInstance Win32_ShadowStorage |
    Select-Object Volume,DiffVolume,UsedSpace,AllocatedSpace,MaxSpace
vssadmin.exe list shadowstorage
vssadmin.exe list shadows
dism.exe /Online /Cleanup-Image /AnalyzeComponentStore /English
fsutil.exe fsinfo ntfsinfo C:
Get-AppxPackage | Select-Object Name,InstallLocation
```

DISM error 740 and vssadmin elevation errors mean the current token is insufficient. Even an administrator may not enumerate System Volume Information or other protected stores. Current-user AppX paths can supplement an unreadable WindowsApps root but do not prove coverage of other users or staged versions. An administrator may use `Get-AppxPackage -AllUsers` for a wider list.

DISM reports shared Windows bytes, backups/disabled features, temporary bytes, and reclaimable package count. Neither all of WinSxS nor all reported backup bytes are guaranteed recoverable. MFT size, VSS allocation, unreadable files, alternate streams, and live changes can explain differences from file totals. Do not simply add VSS to a scan that already included its files.

## Source references

- [FileStandardInfo allocation](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_standard_info)
- [GetCompressedFileSizeW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getcompressedfilesizew)
- [Hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [WinSxS actual size](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/determine-the-actual-size-of-the-winsxs-folder?view=windows-11)
