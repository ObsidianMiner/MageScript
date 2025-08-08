@echo off
REM Run the PowerShell setup script with RemoteSigned execution policy temporarily

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"

echo.
echo Setup complete. Press any key to exit...
pause >nul