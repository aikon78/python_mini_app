# python_mini_app

Mini app Python con GUI per convertire date in file `.txt`/`.csv` dal formato USA
(`m/d/YYYY HH:MM:SS`) al formato italiano (`dd/mm/YYYY HH:MM:SS`) ed esportare in
un file Excel `.xlsx`.

## Avvio

```bash
python app.py
```

## App portable Windows (senza installazione)

Si, puoi distribuire l'app senza installazione.

In questo repository e presente un workflow GitHub Actions che genera una build
portable Windows usando Python embeddable ufficiale (python.org) + script dell'app.
Questa modalita evita exe compilati dal progetto ed e in genere meno soggetta a falsi
positivi rispetto a PyInstaller/Nuitka.

### Come generarlo

1. Pubblica le modifiche su GitHub.
2. Apri la scheda `Actions` del repository.
3. Avvia il workflow `Build Windows Portable App`.
4. Al termine scarica l'artefatto `python-mini-app-windows-portable`.

L'archivio contiene la cartella `portable-app`: estraila e avvia:

- `start_gui.bat` per la GUI
- `start_cli.bat` per l'uso da terminale

### Build locale su Windows

Se vuoi creare la build portable in locale su Windows, scarica il pacchetto
embeddable ufficiale di Python 3.12 x64 e copia nella stessa cartella:

- `app.py`
- `converter.py`
- un file batch launcher (come `start_gui.bat`)

Esempio launcher GUI:

```bash
@echo off
cd /d %~dp0
start "" pythonw.exe app.py
```

Distribuisci la cartella completa in uno zip.

## Funzioni principali

- Selezione multipla di file `.txt` o `.csv`
- Conversione automatica delle date nel formato richiesto
- Esportazione in un unico file `.xlsx` con un foglio per ciascun file input
