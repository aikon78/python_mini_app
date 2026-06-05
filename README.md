# python_mini_app

Mini app Python con GUI per convertire date in file `.txt`/`.csv` dal formato USA
(`m/d/YYYY HH:MM:SS`) al formato italiano (`dd/mm/YYYY HH:MM:SS`) ed esportare in
un file Excel `.xlsx`.

## Avvio

Per aprire la GUI:

```bash
python app.py
```

## Uso da CLI

Puoi usare lo stesso entrypoint anche da terminale:

```bash
python app.py --input file1.csv file2.txt --output risultato.xlsx
```

Argomenti:

- `--input`: uno o piu file `.txt` o `.csv`
- `--output`: file `.xlsx` finale da generare

## Eseguibile console Windows

Se vuoi creare un eseguibile console su Windows, usa PyInstaller senza modalita windowed:

```bash
py -m pip install pyinstaller
py -m PyInstaller --noconfirm --clean --onefile --name app app.py
```

Il file finale verra creato nella cartella `dist`.

## Funzioni principali

- Selezione multipla di file `.txt` o `.csv` via GUI
- Utilizzo da CLI con piu file input
- Conversione automatica delle date nel formato richiesto
- Esportazione in un unico file `.xlsx` con un foglio per ciascun file input
