# python_mini_app

Mini app Python con GUI per convertire date in file `.txt`/`.csv` dal formato USA
(`m/d/YYYY HH:MM:SS`) al formato italiano (`dd/mm/YYYY HH:MM:SS`) ed esportare in
un file Excel `.xlsx`.

## Avvio

```bash
python app.py
```

## Eseguibile Windows `.exe`

### Download (consigliato)

Ogni push su `main` pubblica automaticamente il file `DateConverter.exe` come
artefatto della GitHub Action **Build standalone Windows .exe**.

Per scaricarlo:
1. Vai su **Actions** → **Build standalone Windows .exe** → ultima esecuzione riuscita
2. Nella sezione **Artifacts** scarica `DateConverter-windows`
3. Estrai lo zip ed esegui `DateConverter.exe` — nessuna installazione richiesta

Quando viene creato un tag `vX.Y.Z` il file viene allegato automaticamente anche
alla pagina **Releases**.

### Build locale

Requisiti: Python 3.10+ e PyInstaller installato.

```bash
pip install pyinstaller==6.13.0
pyinstaller DateConverter.spec
```

L'eseguibile viene generato in `dist/DateConverter.exe`.

## Funzioni principali

- Selezione multipla di file `.txt` o `.csv`
- Conversione automatica delle date nel formato richiesto
- Esportazione in un unico file `.xlsx` con un foglio per ciascun file input
