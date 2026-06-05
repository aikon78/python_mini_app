# python_mini_app

Mini app Python con GUI per convertire date in file `.txt`/`.csv` dal formato USA
(`m/d/YYYY HH:MM:SS`) al formato italiano (`dd/mm/YYYY HH:MM:SS`) ed esportare in
un file Excel `.xlsx`.

## Avvio

```bash
python app.py
```

## Uso da CLI

Puoi usare lo stesso entrypoint anche da terminale, senza GUI:

```bash
python app.py --input file1.csv file2.txt --output risultato.xlsx
```

Argomenti:

- `--input`: uno o piu file `.txt` o `.csv`
- `--output`: file `.xlsx` finale da generare

## Eseguibile Windows `.exe`

Si, puoi distribuire l'app come file `.exe` standalone, senza richiedere
un'installazione di Python sul PC finale.

In questo repository e presente un workflow GitHub Actions che genera il file
eseguibile su Windows usando PyInstaller. Questo e il modo piu semplice se stai
lavorando da Linux.

### Come generarlo

1. Pubblica le modifiche su GitHub.
2. Apri la scheda `Actions` del repository.
3. Avvia il workflow `Build Windows EXE`.
4. Al termine scarica l'artefatto `python-mini-app-windows-exe`.

L'archivio contiene `app.exe`, che puo essere eseguito senza installare Python.

### Build locale su Windows

Se vuoi creare l'eseguibile in locale, esegui questi comandi su Windows:

```bash
py -m pip install pyinstaller
py -m PyInstaller --noconfirm --clean --onefile --windowed --name app app.py
```

Il file finale verra creato nella cartella `dist`.

## Funzioni principali

- Selezione multipla di file `.txt` o `.csv`
- Conversione automatica delle date nel formato richiesto
- Esportazione in un unico file `.xlsx` con un foglio per ciascun file input
