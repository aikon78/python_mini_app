@echo off
cd /d "%~dp0"
pythonw "%~dp0avvia.pyw" 2>nul
if errorlevel 1 python "%~dp0avvia.pyw"
