# Skill Conductor Universal Installer for Windows PowerShell
# Usage: iex (irm https://raw.githubusercontent.com/imMamdouhaboammar/skill-conductor/main/install.ps1)

$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "         Skill Conductor Windows Installer        " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Check Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $python) {
    Write-Error "Python 3 is required. Please install Python from https://www.python.org/ or 'winget install Python.Python.3.12'"
    exit 1
}

$InstallDir = Join-Path $HOME ".skill-conductor"
$BinDir = Join-Path $HOME ".local\bin"

if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}
if (-not (Test-Path $BinDir)) {
    New-Item -ItemType Directory -Path $BinDir -Force | Out-Null
}

Write-Host "==> Downloading Skill Conductor into $InstallDir..." -ForegroundColor Blue

$git = Get-Command git -ErrorAction SilentlyContinue
if ($git) {
    if (Test-Path (Join-Path $InstallDir ".git")) {
        git -C $InstallDir pull --quiet
    } else {
        git clone --depth=1 --quiet https://github.com/imMamdouhaboammar/skill-conductor.git $InstallDir
    }
} else {
    $zipUrl = "https://github.com/imMamdouhaboammar/skill-conductor/archive/refs/heads/main.zip"
    $zipFile = Join-Path $InstallDir "repo.zip"
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile
    Expand-Archive -Path $zipFile -DestinationPath $InstallDir -Force
    Remove-Item $zipFile
}

# Create wrapper script skill-conductor.cmd
$cmdPath = Join-Path $BinDir "skill-conductor.cmd"
$entryPoint = Join-Path $InstallDir "bin\skill-conductor"
Set-Content -Path $cmdPath -Value "@echo off`r`npython `"$entryPoint`" %*"

# Check Path
$userPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User)
if ($userPath -notlike "*$BinDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$BinDir", [EnvironmentVariableTarget]::User)
    Write-Host "[NOTE] Added $BinDir to User PATH." -ForegroundColor Yellow
}

Write-Host "`n[OK] Skill Conductor successfully installed!" -ForegroundColor Green
Write-Host "Run 'skill-conductor doctor' in a new PowerShell window to verify." -ForegroundColor Cyan
