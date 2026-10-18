# Registry sweep reference

Enumeration for each record area, the exclusion list for Windows-internal data, and the restore recipe. Commands are PowerShell; run machine-hive operations from one elevated child process.

## 1. Product records

Uninstall entries live in three places and all three matter:

```powershell
$hives = @(
  'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
  'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall',
  'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
)
foreach ($hive in $hives) {
  Get-ChildItem $hive | ForEach-Object {
    $p = Get-ItemProperty $_.PSPath
    if ($p.InstallLocation -like 'D:*' -or $p.InstallSource -like 'd:*') {
      [pscustomobject]@{ Key = $_.PSChildName; Name = $p.DisplayName; Location = $p.InstallLocation }
    }
  }
}
```

Judge a hit by `InstallLocation`, `InstallSource`, and the target directory. The display name is not evidence: vendors leave the name and blank the location.

## 2. Steam

- Library roots: `steamapps\libraryfolders.vdf` under the Steam install, plus `config\libraryfolders.vdf`. Both list each library path and its app IDs.
- Installed games: `steamapps\appmanifest_<appid>.acf` in each live library.
- Per-app state: `HKCU\Software\Valve\Steam\Apps\<appid>`, `HKLM\SOFTWARE\WOW6432Node\Valve\Steam\Apps\<appid>`.
- Uninstall entries: `HKLM\...\Uninstall\Steam App <appid>`.
- Steam root: `HKCU\Software\Valve\Steam` (`SteamPath`, `SteamExe`).

Delete a library block, then confirm both VDF copies hold only live roots. An app with no manifest in any library is not installed, whatever its `Installed` flag says.

## 3. Raw reference scan

Scan for values whose data is a path under the dead root. This is the pass that finds records no product-specific sweep knows about.

```powershell
function Scan-Hive([Microsoft.Win32.RegistryKey]$key, [string]$path, [System.Collections.Generic.List[string]]$list) {
  foreach ($name in $key.GetValueNames()) {
    try {
      $value = $key.GetValue($name)
      if ($value -is [string] -and $value -match '(?i)(^|[^A-Za-z])[Dd]:\\') {
        $list.Add("$path`t$name`t$value")
      }
    } catch {}
  }
  foreach ($sub in $key.GetSubKeyNames()) {
    try {
      $child = $key.OpenSubKey($sub)
      if ($child) { Scan-Hive $child "$path\$sub" $list; $child.Close() }
    } catch {}
  }
}
$hits = New-Object 'System.Collections.Generic.List[string]'
$user = [Microsoft.Win32.RegistryKey]::OpenBaseKey([Microsoft.Win32.RegistryHive]::CurrentUser, [Microsoft.Win32.RegistryView]::Registry64)
Scan-Hive $user 'HKCU' $hits; $user.Close()
$machine = [Microsoft.Win32.RegistryKey]::OpenBaseKey([Microsoft.Win32.RegistryHive]::LocalMachine, [Microsoft.Win32.RegistryView]::Registry64)
Scan-Hive $machine 'HKLM' $hits; $machine.Close()
```

`reg query <hive> /f "D:\" /s /d` gives a faster substring pass, but it cannot see values whose data is binary or whose *name* is the path. Use both.

## 4. Firewall rules

Rules are keyed by program path, and one app can own several (inbound allow per profile):

```powershell
Get-NetFirewallRule | ForEach-Object {
  $app = $_ | Get-NetFirewallApplicationFilter
  if ($app.Program -like 'D:*') { "$($_.Name) $($app.Program)" }
}
Remove-NetFirewallRule -Name '{GUID}'
```

Take a full-policy restore point first with `netsh advfirewall export <path>.wfw`; restore with `netsh advfirewall import <path>.wfw`. Rules reappear when the app runs again from a live path.

## 5. Services, drivers, and first-boot registrations

```powershell
Get-CimInstance Win32_Service | Where-Object { $_.PathName -like '*D:\*' }
sc.exe delete <service>
```

A stopped kernel driver with a missing binary is safe to delete as a service. Also check `HKLM\SYSTEM\Setup\FirstBoot\Services\<name>` — pending first-boot service registrations for drivers that will never exist, and `Get-ScheduledTask` actions whose `Execute` or `Arguments` point at the dead root.

## 6. File associations and App Paths

- `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\<exe>` and its `WOW6432Node` mirror; `HKCU\...\App Paths\<exe>` holds per-user entries. Check both the `(default)` value and `InstallPath`.
- `HKLM\SOFTWARE\Classes\<ProgID>\shell\open\command`, `DefaultIcon`, and protocol handlers under `HKLM\SOFTWARE\Classes\<scheme>`; the user-hive equivalent lives under `HKCU\Software\Classes\...`, and some installers write a malformed handler at `HKCU\<scheme>`.

## 7. App-state caches keyed by path

| Location | Where the path lives |
| --- | --- |
| `HKCU\...\Shell\MuiCache` | value *name*: `<path>.FriendlyAppName` |
| `HKCU\...\Explorer\FeatureUsage\AppSwitched`, `AppBadgeUpdated` | value *name* |
| `HKCU\System\GameConfigStore\Children\<guid>` | `MatchedExeFullPath` |
| `HKCU\...\AppCompatFlags\Compatibility Assistant\Store` | `REG_BINARY`, value *name* is the path |
| `HKCU\Control Panel\NotifyIconSettings\<id>` | `ExecutablePath` |
| `HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache` | same store as above |

Delete the individual value or child key; never delete the parent store.

## 8. Orphaned MSI registrations

An MSI product owns an `Uninstall\{GUID}` key plus an `Installer\UserData\<SID>\Products\<packed>` registration. To pack a product code, take the first three GUID groups and reverse their bytes: `{DDAB335A-D2ED-45F8-A921-8597CC411E20}` becomes `A533BADDDE2D8F549A125879CC14E102`. Search every `UserData\<SID>` tree for the display name before calling the `Uninstall` key orphaned. A live product uninstalls with `msiexec /X{GUID} /qn /norestart`; a product with both registration and directory gone is safe to delete as an orphan.

## 9. Empty install directories

```powershell
Get-ChildItem <dir> -Recurse -File -Force -ErrorAction SilentlyContinue
```

Delete only when the count is zero, and remove `Program Files` / `ProgramData` trees from the elevated process.

## 10. Windows-internal records: keep and explain

| Area | Why it stays |
| --- | --- |
| `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\Packages\...\InstallLocation` | Windows servicing metadata for installed packages |
| `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\...\InstallProperties\InstallSource` | original MSI source for installed products |
| `HKLM\SYSTEM\CurrentControlSet\Services\EventLog\Application\<source>\EventMessageFile` | message catalog location |
| `HKLM\DRIVERS\DriverDatabase\...\OemPath` | driver package origin |
| `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Appx\PackageVolumes\...\SisPath` | Appx volume configuration |

Mention these in the report as expected hits, so the re-scan's nonzero count reads as understood rather than unfinished.

## 11. Restore recipe

Repeat the format in the backup folder's restore note; the user must be able to undo without guessing:

```powershell
reg import .\<backup>.reg
netsh advfirewall import .\firewall-policy.wfw
Copy-Item .\libraryfolders.vdf "C:\Program Files (x86)\Steam\config\libraryfolders.vdf" -Force
Copy-Item .\libraryfolders.vdf "C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf" -Force
```

For an uninstalled MSI component, the registry import alone does not restore files: record in the note that the component returns when the owning app is reinstalled.
