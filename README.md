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
portable Windows usando Nuitka in modalita standalone (cartella con exe + runtime).
Questa modalita e in genere meno soggetta a falsi positivi rispetto a PyInstaller onefile.

### Come generarlo

1. Pubblica le modifiche su GitHub.
2. Apri la scheda `Actions` del repository.
3. Avvia il workflow `Build Windows Portable App`.
4. Al termine scarica l'artefatto `python-mini-app-windows-portable`.

L'archivio contiene la cartella `app.dist`: estraila e avvia `app.exe`.

### Build locale su Windows

Se vuoi creare la build portable in locale su Windows, esegui questi comandi:

```bash
py -m pip install --upgrade nuitka ordered-set zstandard
py -m nuitka app.py --standalone --enable-plugin=tk-inter --windows-console-mode=disable --assume-yes-for-downloads --output-filename=app.exe
```

La build finale verra creata in `app.dist`.

## Funzioni principali

- Selezione multipla di file `.txt` o `.csv`
- Conversione automatica delle date nel formato richiesto
- Esportazione in un unico file `.xlsx` con un foglio per ciascun file input
