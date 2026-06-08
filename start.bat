@echo off
cd /d "%~dp0"

if exist "%~dp0pythonw.exe" (
set "TCL_LIBRARY=%~dp0tcl\tcl8.6"
set "TK_LIBRARY=%~dp0tcl\tk8.6"
"%~dp0pythonw.exe" "%~dp0avvia.pyw"
goto :eof
)

where pythonw >nul 2>nul
if not errorlevel 1 (
pythonw "%~dp0avvia.pyw"
goto :eof
)

python "%~dp0avvia.pyw"
