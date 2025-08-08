# Enable strict error handling
$ErrorActionPreference = 'Stop'

# Define paths
$projectDir = $PSScriptRoot
$scriptName = "interpret"
$pythonScript = Join-Path $projectDir "$scriptName.py"
$wrapperScript = Join-Path $projectDir "$scriptName.cmd"
$pythonInstallPath = "$env:LOCALAPPDATA\Programs\Python\Python312"

Write-Host "Checking for Python..."
$pythonExists = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonExists) {
    Write-Host "Python not found. Installing Python 3.12..."

    $installerPath = Join-Path $projectDir "python-installer.exe"
    $pythonUri = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"

    Invoke-WebRequest -Uri $pythonUri -OutFile $installerPath

    Start-Process -FilePath $installerPath -ArgumentList '/quiet', 'InstallAllUsers=1', 'PrependPath=1', 'Include_test=0' -Wait
    Remove-Item $installerPath -Force

    $pythonExists = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonExists) {
        Write-Error "Python installation failed. Aborting setup."
        exit 1
    }

    Write-Host "Python installed successfully."
} else {
    Write-Host "Python is already installed."
}

Write-Host "`nCreating wrapper script: $wrapperScript"
Set-Content -Path $wrapperScript -Value "@echo off`npython `"$pythonScript`" %*"

$pathsToAdd = @(
    $projectDir.TrimEnd('\'),
    "$pythonInstallPath",
    "$pythonInstallPath\Scripts"
)

$currentUserPath = [Environment]::GetEnvironmentVariable("Path", "User")
$splitPath = $currentUserPath -split ';' | ForEach-Object { $_.Trim() }

foreach ($path in $pathsToAdd) {
    if (-not ($splitPath -contains $path)) {
        Write-Host "Adding to PATH: $path"
        $splitPath += $path
    } else {
        Write-Host "Already in PATH: $path"
    }
}

$newUserPath = ($splitPath -join ';').Trim(';')
[Environment]::SetEnvironmentVariable("Path", $newUserPath, "User")

Write-Host "Setup complete."
Write-Host "Open a NEW terminal to use the 'interpret' command."
