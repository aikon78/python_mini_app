# python_mini_app

Mini app Python con GUI per convertire date in file `.txt`/`.csv` dal formato USA
(`m/d/YYYY HH:MM:SS`) al formato italiano (`dd/mm/YYYY HH:MM:SS`) ed esportare in
un file Excel `.xlsx`.

## Avvio

```bash
python app.py
```

## CI con GitHub Actions

Il repository esegue una pipeline CI automatica su GitHub Actions ad ogni push su
`main` e su ogni pull request.

La pipeline (`CI`) verifica il progetto su Python 3.11 e 3.12 ed esegue:

- aggiornamento `pip`
- test unitari (`python -m unittest discover -s tests -p "test_*.py" -v`)

Puoi consultare l'esito nella scheda `Actions` del repository.

## App Windows

Il workflow `buildalo` genera un archivio zip
`python-mini-app-windows.zip` con i sorgenti dell'app e i launcher per Windows.

**Requisito:** Python deve essere già installato sulla macchina Windows.

**Perché resta semplice da distribuire:**
- I file launcher (`avvia.pyw`, `start.bat`) sono **codice sorgente statico
  committato nel repository**, non generati a runtime — elimina il pattern
  "script genera script" che causa i falsi positivi.

**Non richiede diritti di amministratore** per la build. Per l'esecuzione basta
un'installazione standard di Python già presente nel sistema.

### Come generare l'artefatto

1. Pubblica le modifiche su GitHub.
2. Apri la scheda `Actions` del repository.
3. Avvia il workflow `buildalo`.
4. Al termine scarica `python-mini-app-windows`.

### Avvio su Windows

Estrai lo zip e fai doppio clic su **`start.bat`**.

Il launcher usa il Python installato nel sistema (`pyw`, `pythonw`, `py` o
`python`, in quest'ordine) e apre l'app GUI.

## Funzioni principali

- Selezione multipla di file `.txt` o `.csv`
- Conversione automatica delle date nel formato richiesto
- Esportazione in un unico file `.xlsx` con un foglio per ciascun file input
