@echo off
cd /d "%~dp0"
set "LOG_FILE=%~dp0startup-error.log"

where pyw >nul 2>nul
if not errorlevel 1 (
pyw "%~dp0avvia.pyw"
goto :eof
)

where pythonw >nul 2>nul
if not errorlevel 1 (
pythonw "%~dp0avvia.pyw"
goto :eof
)

where py >nul 2>nul
if not errorlevel 1 (
py "%~dp0avvia.pyw"
goto :eof
)

where python >nul 2>nul
if not errorlevel 1 (
python "%~dp0avvia.pyw"
goto :eof
)

>>"%LOG_FILE%" echo [%date% %time%] Nessun interprete Python trovato.
echo Avvio non riuscito. Controlla il log: "%LOG_FILE%"
pause
