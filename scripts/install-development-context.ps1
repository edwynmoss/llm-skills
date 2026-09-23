#Requires -Version 7.0
[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$SkillsDirectory = (Join-Path $env:USERPROFILE '.agents/skills'),
    [string]$CodexDirectory = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }),
    [ValidateSet('User', 'Process')][string]$EnvironmentTarget = 'User',
    [switch]$UpdateSkills,
    [ValidateSet('ui-ux', 'backend')][string]$LibraryKind = 'ui-ux'
)
$ErrorActionPreference = 'Stop'
$package = Split-Path $PSScriptRoot -Parent
$library = if ($LibraryKind -eq 'backend') {
    @{Docs='docs/backend'; Prefix='backend'; Environment='BACKEND_DOCS_ROOT'; Label='Backend'; Marker='backend-context'; Heading='## Backend skills and shared standards'}
} else {
    @{Docs='docs/ux'; Prefix='ui'; Environment='UI_UX_DOCS_ROOT'; Label='UI/UX'; Marker='ui-ux-context'; Heading='## UI/UX skills and shared standards'}
}
$docs = [IO.Path]::GetFullPath((Join-Path $package $library.Docs))
$SkillsDirectory = [IO.Path]::GetFullPath($SkillsDirectory)
$CodexDirectory = [IO.Path]::GetFullPath($CodexDirectory)
$names = @('spec', 'build', 'verify') | ForEach-Object { $library.Prefix + '-' + $_ }
$utf8 = [Text.UTF8Encoding]::new($false)
$writes = [ordered]@{}
$originals = @{}
$createdDirectories = [Collections.Generic.List[string]]::new()

function Add-ManagedWrite([string]$Path, [string]$Content, [bool]$RequireUpdate) {
    if (Test-Path -LiteralPath $Path -PathType Container) { throw "Expected file, found directory: $Path" }
    $existing = if (Test-Path -LiteralPath $Path) { [IO.File]::ReadAllText($Path) } else { $null }
    if ($null -ne $existing -and $existing -ceq $Content) { return }
    if ($null -ne $existing -and $RequireUpdate -and -not $UpdateSkills) {
        throw "Existing managed file differs: $Path. Review it, then use -UpdateSkills."
    }
    $writes[$Path] = $Content
    $originals[$Path] = if ($null -ne $existing) { [IO.File]::ReadAllBytes($Path) } else { $null }
}

foreach ($required in @('governance.md', 'codex-global-instructions.md', 'modules/verification.md')) {
    if (-not (Test-Path -LiteralPath (Join-Path $docs $required) -PathType Leaf)) { throw "Shared library is incomplete: $required" }
}
$override = Join-Path $CodexDirectory 'AGENTS.override.md'
if ((Test-Path -LiteralPath $override) -and (Get-Item -LiteralPath $override).Length -gt 0) {
    throw 'AGENTS.override.md supersedes global guidance. Reconcile it before installation.'
}
foreach ($name in $names) {
    $destination = Join-Path $SkillsDirectory "$name/SKILL.md"
    $legacy = Join-Path $CodexDirectory "skills/$name/SKILL.md"
    if ((Test-Path -LiteralPath $legacy) -and [IO.Path]::GetFullPath($legacy) -ne [IO.Path]::GetFullPath($destination)) {
        throw "Duplicate discovery risk for $name. Use -SkillsDirectory for the existing location."
    }
    $modern = Join-Path (Split-Path $CodexDirectory -Parent) ".agents/skills/$name/SKILL.md"
    if ((Test-Path -LiteralPath $modern) -and [IO.Path]::GetFullPath($modern) -ne [IO.Path]::GetFullPath($destination)) {
        throw "Duplicate discovery risk for $name in the user .agents location."
    }
    $source = Join-Path $package "skills/$name/SKILL.md"
    $content = [IO.File]::ReadAllText($source)
    # Every explicit library reference must exist before any installation writes.
    foreach ($match in [regex]::Matches($content, '`((?:(?:modules|templates)/)?[a-z][a-z0-9-]*\.md)`')) {
        if (-not (Test-Path -LiteralPath (Join-Path $docs $match.Groups[1].Value) -PathType Leaf)) {
            throw "Unresolved reference in ${name}: $($match.Groups[1].Value)"
        }
    }
    Add-ManagedWrite $destination $content $true
    Add-ManagedWrite (Join-Path $SkillsDirectory "$name/library-root.txt") ($docs + "`n") $true
}

$instructionPath = Join-Path $CodexDirectory 'AGENTS.md'
$existingGuidance = if (Test-Path -LiteralPath $instructionPath) { [IO.File]::ReadAllText($instructionPath) } else { '' }
$start = '<!-- ' + $library.Marker + ':start -->'
$end = '<!-- ' + $library.Marker + ':end -->'
$guidance = [IO.File]::ReadAllText((Join-Path $docs 'codex-global-instructions.md')).TrimEnd()
$block = "$start`n$guidance`n$end"
$pattern = '(?s)' + [regex]::Escape($start) + '.*?' + [regex]::Escape($end)
if ($existingGuidance.Contains($start) -or $existingGuidance.Contains($end)) {
    if ([regex]::Matches($existingGuidance, $pattern).Count -ne 1 -or
        [regex]::Matches($existingGuidance, [regex]::Escape($start)).Count -ne 1 -or
        [regex]::Matches($existingGuidance, [regex]::Escape($end)).Count -ne 1) {
        throw "Ambiguous $($library.Label) instruction markers; global instructions preserved."
    }
    $updatedGuidance = [regex]::Replace($existingGuidance, $pattern, [Text.RegularExpressions.MatchEvaluator]{ param($match) $block })
} elseif ($existingGuidance.Contains($library.Heading)) {
    throw "Unmanaged $($library.Label) instructions already exist. Reconcile them before adding a managed block."
} else {
    $updatedGuidance = $existingGuidance + "`n`n" + $block + "`n"
}
# Never rewrite unrelated TOML. Stop if the existing/default instruction budget is insufficient.
$configPath = Join-Path $CodexDirectory 'config.toml'
$config = if (Test-Path -LiteralPath $configPath) { [IO.File]::ReadAllText($configPath) } else { '' }
$rootConfig = ($config -split '(?m)^\s*\[', 2)[0]
$limitMatch = [regex]::Match($rootConfig, '(?m)^project_doc_max_bytes\s*=\s*(\d+)\s*(?:#.*)?$')
if ($rootConfig -match '(?m)^\s*project_doc_max_bytes\s*=' -and -not $limitMatch.Success) { throw 'Unrecognised instruction-budget setting; configuration preserved.' }
$limit = if ($limitMatch.Success) { [long]$limitMatch.Groups[1].Value } else { 32768 }
if ($utf8.GetByteCount($updatedGuidance) -gt $limit) { throw 'Global instructions exceed the configured document budget. Resolve the budget before installation; no configuration changed.' }
Add-ManagedWrite $instructionPath $updatedGuidance $false
$previousEnvironment = [Environment]::GetEnvironmentVariable($library.Environment, $EnvironmentTarget)
$previousProcess = [Environment]::GetEnvironmentVariable($library.Environment, 'Process')
if ($previousEnvironment -and [IO.Path]::GetFullPath($previousEnvironment) -ne $docs -and -not $UpdateSkills) {
    throw "$($library.Environment) already points elsewhere. Review the library change and use -UpdateSkills."
}

if ($PSCmdlet.ShouldProcess($SkillsDirectory, "Install three $($library.Label) skills, shared-library locators and managed global routing")) {
    $applied = [Collections.Generic.List[string]]::new()
    try {
        foreach ($entry in $writes.GetEnumerator()) {
            $parent = Split-Path $entry.Key -Parent
            $missing = [Collections.Generic.List[string]]::new()
            while (-not (Test-Path -LiteralPath $parent)) { $missing.Add($parent); $parent = Split-Path $parent -Parent }
            for ($i = $missing.Count - 1; $i -ge 0; $i--) {
                New-Item -ItemType Directory -Path $missing[$i] | Out-Null
                $createdDirectories.Add($missing[$i])
            }
            $applied.Add($entry.Key)
            [IO.File]::WriteAllText($entry.Key, $entry.Value, $utf8)
            if ([IO.File]::ReadAllText($entry.Key) -cne $entry.Value) { throw "Readback failed: $($entry.Key)" }
        }
        [Environment]::SetEnvironmentVariable($library.Environment, $docs, $EnvironmentTarget)
        [Environment]::SetEnvironmentVariable($library.Environment, $docs, 'Process')
    } catch {
        for ($i = $applied.Count - 1; $i -ge 0; $i--) {
            $path = $applied[$i]
            if ($null -eq $originals[$path]) { Remove-Item -LiteralPath $path -Force }
            else { [IO.File]::WriteAllBytes($path, $originals[$path]) }
        }
        for ($i = $createdDirectories.Count - 1; $i -ge 0; $i--) {
            if (-not (Get-ChildItem -LiteralPath $createdDirectories[$i] -Force)) { [IO.Directory]::Delete($createdDirectories[$i]) }
        }
        [Environment]::SetEnvironmentVariable($library.Environment, $previousEnvironment, $EnvironmentTarget)
        [Environment]::SetEnvironmentVariable($library.Environment, $previousProcess, 'Process')
        throw
    }
    [pscustomobject]@{
        Installed = $true; Skills = 3; ChangedFiles = $writes.Count
        Documentation = $docs; SkillsDirectory = $SkillsDirectory; Instructions = $instructionPath
        EnvironmentChanged = ($previousEnvironment -cne $docs)
        ConfigurationChanged = $false
    } | ConvertTo-Json -Compress
}
