from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from converter import convert_files_to_excel


class DateConverterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Date Converter TXT/CSV -> Excel")
        self.root.geometry("760x460")
        self.selected_files: list[Path] = []
        self.output_file: Path | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        frame = tk.Frame(self.root, padx=12, pady=12)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Seleziona uno o più file TXT/CSV da convertire in formato italiano",
            anchor="w",
        ).pack(fill="x")

        self.file_listbox = tk.Listbox(frame, height=12, selectmode=tk.EXTENDED)
        self.file_listbox.pack(fill="both", expand=True, pady=(10, 8))

        files_button_row = tk.Frame(frame)
        files_button_row.pack(fill="x", pady=(0, 12))
        tk.Button(files_button_row, text="Aggiungi file", command=self.add_files).pack(
            side="left"
        )
        tk.Button(
            files_button_row,
            text="Rimuovi selezionati",
            command=self.remove_selected_files,
        ).pack(side="left", padx=8)

        output_row = tk.Frame(frame)
        output_row.pack(fill="x", pady=(0, 12))
        tk.Button(output_row, text="Scegli file Excel output", command=self.choose_output).pack(
            side="left"
        )
        self.output_label = tk.Label(output_row, text="Output: non selezionato", anchor="w")
        self.output_label.pack(side="left", fill="x", expand=True, padx=10)

        tk.Button(frame, text="Converti in Excel", command=self.convert).pack(anchor="e")

        self.status_label = tk.Label(frame, text="", fg="green", anchor="w")
        self.status_label.pack(fill="x", pady=(8, 0))

    def add_files(self) -> None:
        paths = filedialog.askopenfilenames(
            title="Seleziona file TXT o CSV",
            filetypes=[("File di testo e CSV", "*.txt *.csv"), ("Tutti i file", "*.*")],
        )
        for raw_path in paths:
            path = Path(raw_path)
            if path not in self.selected_files:
                self.selected_files.append(path)
                self.file_listbox.insert(tk.END, str(path))

        if self.selected_files and self.output_file is None:
            default_output = self.selected_files[0].with_name(
                f"{self.selected_files[0].stem}_convertito.xlsx"
            )
            self.output_file = default_output
            self.output_label.configure(text=f"Output: {self.output_file}")

    def remove_selected_files(self) -> None:
        selection = list(self.file_listbox.curselection())
        for index in reversed(selection):
            self.file_listbox.delete(index)
            del self.selected_files[index]

    def choose_output(self) -> None:
        selected = filedialog.asksaveasfilename(
            title="Salva file Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel Workbook", "*.xlsx")],
        )
        if selected:
            self.output_file = Path(selected)
            self.output_label.configure(text=f"Output: {self.output_file}")

    def convert(self) -> None:
        if not self.selected_files:
            messagebox.showwarning("Attenzione", "Seleziona almeno un file TXT o CSV.")
            return
        if self.output_file is None:
            messagebox.showwarning("Attenzione", "Scegli il file di output Excel.")
            return

        try:
            convert_files_to_excel(self.selected_files, self.output_file)
        except Exception as exc:  # noqa: BLE001 - GUI surface for conversion errors
            messagebox.showerror("Errore", f"Conversione fallita: {exc}")
            self.status_label.configure(text="", fg="red")
            return

        self.status_label.configure(text=f"File creato: {self.output_file}", fg="green")
        messagebox.showinfo("Completato", f"Conversione terminata.\n{self.output_file}")


def main() -> None:
    root = tk.Tk()
    app = DateConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
