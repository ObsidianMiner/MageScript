@echo off
REM Run the PowerShell setup script with RemoteSigned execution policy temporarily

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"

echo.
echo The setup has been completed... Let the spells take hold.
pause >nul