from __future__ import annotations

from datetime import datetime
from pathlib import Path
import traceback


LOG_FILE = Path(__file__).with_name("startup-error.log")


def write_startup_error_log() -> Path:
	with LOG_FILE.open("a", encoding="utf-8") as handle:
		handle.write(f"[{datetime.now().isoformat(timespec='seconds')}] Startup failure\n")
		handle.write(traceback.format_exc())
		handle.write("\n")
	return LOG_FILE


try:
	from app import main

	main()
except Exception:
	log_path = write_startup_error_log()

	try:
		import tkinter as tk
		from tkinter import messagebox

		root = tk.Tk()
		root.withdraw()
		messagebox.showerror(
			"Errore avvio",
			f"Avvio non riuscito. Controlla il log:\n{log_path}",
		)
		root.destroy()
	except Exception:
		pass

	raise
