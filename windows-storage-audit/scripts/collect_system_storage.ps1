param(
    [Parameter(Mandatory=$true)][string]$OutputDirectory,
    [switch]$IncludeProtected
)
$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'This collector requires Windows.' }
$outputPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputDirectory)
if (Test-Path -LiteralPath $outputPath) { throw 'Output directory already exists; choose a new snapshot.' }
$ancestor = [IO.DirectoryInfo]::new([IO.Path]::GetDirectoryName($outputPath))
while ($null -ne $ancestor) {
    if ($ancestor.Exists -and ($ancestor.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        throw "Output ancestor is a reparse point: $($ancestor.FullName)"
    }
    $ancestor = $ancestor.Parent
}
New-Item -ItemType Directory -Path $outputPath -ErrorAction Stop | Out-Null
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal]::new($identity)
$elevated = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
$results = [Collections.Generic.List[object]]::new()

function Save-Query([string]$Name, [scriptblock]$Query) {
    try {
        $data = @(& $Query)
        ConvertTo-Json -InputObject $data -Depth 4 |
            Set-Content -LiteralPath (Join-Path $outputPath ($Name + '.json')) -Encoding UTF8
        $results.Add([ordered]@{name=$Name;status='ok';count=$data.Count})
    } catch {
        $results.Add([ordered]@{name=$Name;status='error';message=$_.Exception.Message})
    }
}

function Save-Native([string]$Name, [string]$Executable, [string[]]$Arguments) {
    try {
        $nativeCommand = Get-Command -Name $Executable -CommandType Application -ErrorAction Stop
        $previousPreference = $ErrorActionPreference
        try {
            $ErrorActionPreference = 'Continue'
            & $nativeCommand.Source @Arguments 2>&1 | Out-File -LiteralPath (Join-Path $outputPath ($Name + '.txt')) -Encoding UTF8 -ErrorAction Stop
            $nativeExit = $LASTEXITCODE
        } finally { $ErrorActionPreference = $previousPreference }
        $results.Add([ordered]@{name=$Name;status=$(if ($nativeExit -eq 0) {'ok'} else {'error'});exit_code=$nativeExit})
    } catch {
        $results.Add([ordered]@{name=$Name;status='error';message=$_.Exception.Message})
    }
}

$started = Get-Date -Format o
Save-Query 'disks' { Get-CimInstance Win32_DiskDrive | Select-Object Index,Model,MediaType,Size,InterfaceType }
Save-Query 'logical-disks' { Get-CimInstance Win32_LogicalDisk | Select-Object DeviceID,DriveType,FileSystem,VolumeName,Size,FreeSpace }
Save-Query 'volumes' { Get-Volume | Select-Object DriveLetter,DriveType,FileSystemType,Size,SizeRemaining,AllocationUnitSize }
Save-Query 'pagefile' { Get-CimInstance Win32_PageFileUsage | Select-Object Name,AllocatedBaseSize,CurrentUsage,PeakUsage }
Save-Query 'appx' { Get-AppxPackage | Select-Object Name,InstallLocation }
if ($IncludeProtected) {
    if (-not $elevated) {
        $results.Add([ordered]@{name='protected';status='error';message='Administrator token required. No automatic elevation attempted.'})
    } else {
        Save-Query 'shadowstorage' {
            Get-CimInstance Win32_ShadowStorage | Select-Object @{n='Volume';e={$_.Volume.DeviceID}},@{n='DiffVolume';e={$_.DiffVolume.DeviceID}},UsedSpace,AllocatedSpace,MaxSpace
        }
        Save-Query 'appx-all-users' { Get-AppxPackage -AllUsers | Select-Object Name,InstallLocation }
        Save-Native 'shadowstorage-native' 'vssadmin.exe' @('list','shadowstorage')
        Save-Native 'shadows-native' 'vssadmin.exe' @('list','shadows')
        if (@(Get-Process -Name dism,TiWorker -ErrorAction SilentlyContinue).Count -gt 0) {
            $results.Add([ordered]@{name='component-store';status='error';message='Servicing process active; analysis deferred.'})
        } else {
            Save-Native 'component-store' 'dism.exe' @('/Online','/Cleanup-Image','/AnalyzeComponentStore','/English',('/LogPath:' + (Join-Path $outputPath 'dism.log')))
        }
        try {
            foreach ($volume in @(Get-Volume | Where-Object { $_.DriveLetter -and $_.FileSystemType -eq 'NTFS' })) {
                Save-Native ('ntfs-' + $volume.DriveLetter) 'fsutil.exe' @('fsinfo','ntfsinfo',($volume.DriveLetter + ':'))
            }
        } catch {
            $results.Add([ordered]@{name='ntfs-volume-list';status='error';message=$_.Exception.Message})
        }
    }
}
$partial = @($results | Where-Object { $_.status -ne 'ok' }).Count -gt 0
[ordered]@{started=$started;finished=(Get-Date -Format o);elevated=$elevated;protected_requested=[bool]$IncludeProtected;partial=$partial;queries=$results} |
    ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $outputPath 'summary.json') -Encoding UTF8
[ordered]@{output=$outputPath;partial=$partial;elevated=$elevated;protected_requested=[bool]$IncludeProtected} | ConvertTo-Json -Compress
if ($partial) { exit 2 }
