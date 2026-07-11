# This is just some Claude garbage, but it gets the job done I guess.
# Heck windows.

<#
.SYNOPSIS
    Installs the "giti" PowerShell function so git-informed can be run from any directory.

.DESCRIPTION
    Place this script in the ROOT of the git-informed repo (next to src\ and .venv\) and
    run it from there. It resolves its own location via $PSScriptRoot, so the absolute
    path it bakes in is correct regardless of what your current directory happens to be
    when you invoke it.

    It adds a "giti" function to your PowerShell profile ($PROFILE) that calls this repo's
    virtual environment Python and main.py by absolute path, forwarding through whatever
    arguments you pass (e.g. `giti ..`).

    Safe to re-run: it replaces its own previously-installed block instead of duplicating it.
#>

$ErrorActionPreference = "Stop"

# --- Resolve the absolute path of this repo from the script's own location ---
$repoRoot = $PSScriptRoot
if (-not $repoRoot) {
    # Fallback for edge cases where $PSScriptRoot is blank (e.g. pasted into a console)
    $repoRoot = (Get-Location).Path
    Write-Warning "Could not resolve script location via `$PSScriptRoot; falling back to current directory ($repoRoot). Run install.ps1 directly (not pasted) from the repo root for a reliable path."
}

$pythonExe = Join-Path $repoRoot ".venv\Scripts\python.exe"
$mainPy    = Join-Path $repoRoot "src\main.py"

Write-Host "Repo root:  $repoRoot"
Write-Host "Python exe: $pythonExe"
Write-Host "main.py:    $mainPy"
Write-Host ""

if (-not (Test-Path $pythonExe)) {
    Write-Warning "Could not find '$pythonExe'. Make sure the venv is created (e.g. 'python -m venv .venv' + install requirements) before using 'giti'."
}
if (-not (Test-Path $mainPy)) {
    Write-Warning "Could not find '$mainPy'. Is install.ps1 sitting at the root of git-informed, alongside src\main.py?"
}

# --- Build the function block ---
$marker = "giti-function"
$functionBlock = @"
# >>> $marker >>>
function giti {
    & "$pythonExe" "$mainPy" @args
}
# <<< $marker <<<
"@

# --- Make sure the profile file exists ---
if (-not (Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force | Out-Null
    Write-Host "Created new PowerShell profile at $PROFILE"
}

$existingContent = Get-Content -Path $PROFILE -Raw -ErrorAction SilentlyContinue
if ($null -eq $existingContent) { $existingContent = "" }

# --- Strip any previously-installed block (idempotent re-run), then append fresh block ---
$pattern = "(?ms)\r?\n?# >>> $marker >>>.*?# <<< $marker <<<\r?\n?"
$cleaned = [regex]::Replace($existingContent, $pattern, "")
$newContent = $cleaned.TrimEnd() + "`r`n`r`n$functionBlock`r`n"

Set-Content -Path $PROFILE -Value $newContent
Write-Host "Installed 'giti' function into $PROFILE"
Write-Host ""
Write-Host "Restart your terminal, or run:  . `$PROFILE"
Write-Host "Then use it from anywhere, e.g.:  giti .."