#Requires -Version 7.0
[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$SkillsDirectory = (Join-Path $env:USERPROFILE '.agents/skills'),
    [string]$CodexDirectory = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }),
    [ValidateSet('User', 'Process')][string]$EnvironmentTarget = 'User',
    [switch]$UpdateSkills
)
& (Join-Path $PSScriptRoot 'install-development-context.ps1') -LibraryKind 'ui-ux' @PSBoundParameters
