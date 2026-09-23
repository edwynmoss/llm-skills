#Requires -Version 7.0
param([Parameter(Mandatory)][string]$WorkDirectory, [ValidateSet('ui-ux', 'backend')][string]$LibraryKind = 'ui-ux')
$ErrorActionPreference = 'Stop'
$workRoot = (Resolve-Path -LiteralPath $WorkDirectory).Path
$fixtureRoot = Join-Path $workRoot ('ui-skill-install-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $fixtureRoot | Out-Null
$installer = Join-Path $PSScriptRoot "install-$LibraryKind-context.ps1"
$prefix = if ($LibraryKind -eq 'backend') { 'backend' } else { 'ui' }
$marker = if ($LibraryKind -eq 'backend') { 'backend-context' } else { 'ui-ux-context' }
$names = @('spec', 'build', 'verify') | ForEach-Object { "$prefix-$_" }
$shell = (Get-Process -Id $PID).Path
$checks = [Collections.Generic.List[string]]::new()
$previousProcess = @{}
foreach ($name in @('UI_UX_DOCS_ROOT', 'BACKEND_DOCS_ROOT')) {
    $previousProcess[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
}

function Assert-True($Condition, [string]$Message) { if (-not $Condition) { throw $Message } }
function Invoke-Install([string]$Root, [string[]]$Extra = @(), [bool]$Success = $true) {
    $result = & $shell -NoProfile -File $installer -SkillsDirectory (Join-Path $Root '.agents/skills') -CodexDirectory (Join-Path $Root '.codex') -EnvironmentTarget Process @Extra 2>&1
    $code = $LASTEXITCODE
    Assert-True (($Success -and $code -eq 0) -or (-not $Success -and $code -ne 0)) "Unexpected installer result: $result"
    return ($result | Out-String)
}
try {
    # Child processes only; never modify persistent user environment during tests.
    foreach ($name in $previousProcess.Keys) {
        [Environment]::SetEnvironmentVariable($name, $null, 'Process')
    }
    $first = Join-Path $fixtureRoot 'first'
    New-Item -ItemType Directory -Path (Join-Path $first '.codex') -Force | Out-Null
    $agents = Join-Path $first '.codex/AGENTS.md'
    [IO.File]::WriteAllText($agents, 'Keep unrelated instructions exactly.')
    $preview = Invoke-Install $first @('-WhatIf')
    Assert-True (-not (Test-Path -LiteralPath (Join-Path $first '.agents'))) 'WhatIf wrote skills'
    Assert-True ([IO.File]::ReadAllText($agents) -ceq 'Keep unrelated instructions exactly.') 'WhatIf changed instructions'
    $checks.Add('WhatIf does not write')

    $installed = (Invoke-Install $first) | ConvertFrom-Json
    Assert-True ($installed.ChangedFiles -eq 7) 'Expected six skill/locator files plus instructions'
    Assert-True ([IO.File]::ReadAllText($agents).StartsWith('Keep unrelated instructions exactly.')) 'Unrelated guidance lost'
    foreach ($name in $names) {
        $folder = Join-Path $first ".agents/skills/$name"
        $docs = [IO.File]::ReadAllText((Join-Path $folder 'library-root.txt')).Trim()
        Assert-True (Test-Path -LiteralPath (Join-Path $docs 'governance.md')) 'Library locator broken'
    }
    $checks.Add('First install preserves unrelated guidance and resolves library')
    $again = (Invoke-Install $first) | ConvertFrom-Json
    Assert-True ($again.ChangedFiles -eq 0) 'Repeat install is not idempotent'
    $checks.Add('Repeat install makes zero file changes')

    $otherKind = if ($LibraryKind -eq 'backend') { 'ui-ux' } else { 'backend' }
    $otherInstaller = Join-Path $PSScriptRoot "install-$otherKind-context.ps1"
    $config = Join-Path $first '.codex/config.toml'
    [IO.File]::WriteAllText($config, "project_doc_max_bytes = 65536`n# Preserve configuration.")
    $configBefore = [IO.File]::ReadAllText($config)
    $ownBefore = [IO.File]::ReadAllText($agents)
    $otherResult = & $shell -NoProfile -File $otherInstaller -SkillsDirectory (Join-Path $first '.agents/skills') -CodexDirectory (Join-Path $first '.codex') -EnvironmentTarget Process 2>&1
    Assert-True ($LASTEXITCODE -eq 0) "Second library installation failed: $otherResult"
    Assert-True ([IO.File]::ReadAllText($agents).StartsWith($ownBefore.TrimEnd())) 'Second library changed first managed block'
    $coexisting = [IO.File]::ReadAllText($agents)
    $again = (Invoke-Install $first) | ConvertFrom-Json
    Assert-True ($again.ChangedFiles -eq 0) 'Existing library changed after coexistence install'
    Assert-True ([IO.File]::ReadAllText($agents) -ceq $coexisting) 'Coexistence changed managed guidance'
    Assert-True ([IO.File]::ReadAllText($config) -ceq $configBefore) 'Installer changed configuration'
    Assert-True ((Get-ChildItem -LiteralPath (Join-Path $first '.agents/skills') -Directory).Count -eq 6) 'Both libraries must retain three entries'
    $checks.Add('Both libraries coexist, preserve configuration and remain idempotent')

    $skill = Join-Path $first ".agents/skills/$prefix-build/SKILL.md"
    [IO.File]::AppendAllText($skill, "`nUser-maintained edit.")
    $before = [IO.File]::ReadAllText($agents)
    $null = Invoke-Install $first @() $false
    Assert-True ([IO.File]::ReadAllText($skill).Contains('User-maintained edit.')) 'Conflicting edit overwritten'
    Assert-True ([IO.File]::ReadAllText($agents) -ceq $before) 'Conflict changed guidance'
    $checks.Add('Differing skill rejected before writes')
    $sentinel = Join-Path $first ".agents/skills/$prefix-build/user-notes.txt"
    [IO.File]::WriteAllText($sentinel, 'Preserve me.')
    $updated = (Invoke-Install $first @('-UpdateSkills')) | ConvertFrom-Json
    Assert-True ($updated.ChangedFiles -eq 1) 'Explicit update changed unexpected files'
    Assert-True ([IO.File]::ReadAllText($sentinel) -ceq 'Preserve me.') 'Update removed unrelated file'
    $checks.Add('Explicit update preserves other files')

    $duplicate = Join-Path $fixtureRoot 'duplicate'
    $legacy = Join-Path $duplicate ".codex/skills/$prefix-spec"
    New-Item -ItemType Directory -Path $legacy -Force | Out-Null
    [IO.File]::WriteAllText((Join-Path $legacy 'SKILL.md'), 'Existing skill')
    $null = Invoke-Install $duplicate @() $false
    Assert-True (-not (Test-Path -LiteralPath (Join-Path $duplicate '.agents'))) 'Duplicate created'
    $checks.Add('Legacy duplicate rejected before writes')

    [IO.File]::WriteAllText((Join-Path $first '.codex/AGENTS.override.md'), 'Override')
    $null = Invoke-Install $first @() $false
    Remove-Item -LiteralPath (Join-Path $first '.codex/AGENTS.override.md')
    $checks.Add('Active override rejected')
    [IO.File]::AppendAllText($agents, "`n<!-- ${marker}:start -->")
    $null = Invoke-Install $first @() $false
    $checks.Add('Ambiguous managed block rejected')

    $budget = Join-Path $fixtureRoot 'budget'
    New-Item -ItemType Directory -Path (Join-Path $budget '.codex') -Force | Out-Null
    [IO.File]::WriteAllText((Join-Path $budget '.codex/config.toml'), 'project_doc_max_bytes = 100')
    $null = Invoke-Install $budget @() $false
    Assert-True (-not (Test-Path -LiteralPath (Join-Path $budget '.agents'))) 'Insufficient budget caused partial install'
    $checks.Add('Insufficient instruction budget rejected before writes')
    [pscustomobject]@{Passed=$checks.Count;Checks=$checks} | ConvertTo-Json -Depth 3
} finally {
    foreach ($name in $previousProcess.Keys) {
        [Environment]::SetEnvironmentVariable($name, $previousProcess[$name], 'Process')
    }
    $resolvedFixture = (Resolve-Path -LiteralPath $fixtureRoot).Path
    if ([IO.Path]::GetDirectoryName($resolvedFixture) -ne $workRoot) { throw 'Unsafe fixture cleanup target' }
    Remove-Item -LiteralPath $resolvedFixture -Recurse -Force
}

# Expected rejection cases must not leak a failed native exit code to the runner.
$global:LASTEXITCODE = 0
