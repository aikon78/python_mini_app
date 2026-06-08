@echo off
cd /d "%~dp0"
set "TCL_LIBRARY=%~dp0tcl\tcl8.6"
set "TK_LIBRARY=%~dp0tcl\tk8.6"
start "" pythonw.exe avvia.pyw
