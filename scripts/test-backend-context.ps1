#Requires -Version 7.0
param([Parameter(Mandatory)][string]$WorkDirectory)
& (Join-Path $PSScriptRoot 'test-development-context.ps1') -LibraryKind 'backend' -WorkDirectory $WorkDirectory
