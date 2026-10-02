# Enable strict error handling
$ErrorActionPreference = 'Stop'
#Requires -RunAsAdministrator


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

# Get the current PATH environment variable for the machine
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)

foreach ($newPath in $pathsToAdd) {
    # Check if the new path is already in the PATH variable
    if ($currentPath -notlike "*$newPath*") {
        # If the new path is not in the PATH variable, add it
        $newPathValue = "$currentPath;$newPath"

        try {
            # Set the new PATH environment variable
            [System.Environment]::SetEnvironmentVariable("Path", $newPathValue, [System.EnvironmentVariableTarget]::Machine)
            Write-Output "The path has been added successfully."
        } catch {
            Write-Error "Failed to set the environment variable: $_"
        }
    } else {
        Write-Output "The path is already in the PATH variable."
    }
}

Write-Host "Setup complete."
Write-Host "Open a NEW terminal to use the 'interpret' command."
pip install SpeechRecognition pyaudio