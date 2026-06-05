from __future__ import annotations

import argparse
from pathlib import Path
import sys
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

    def _default_output_file(self) -> Path | None:
        if self.output_file is not None:
            return self.output_file
        if not self.selected_files:
            return None
        return self.selected_files[0].with_name(
            f"{self.selected_files[0].stem}_convertito.xlsx"
        )

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

        default_output = self._default_output_file()
        if default_output is not None and self.output_file is None:
            self.output_file = default_output
            self.output_label.configure(text=f"Output: {self.output_file}")

    def remove_selected_files(self) -> None:
        selection = list(self.file_listbox.curselection())
        for index in reversed(selection):
            self.file_listbox.delete(index)
            del self.selected_files[index]

        if not self.selected_files:
            self.output_file = None
            self.output_label.configure(text="Output: non selezionato")
            self.status_label.configure(text="")

    def choose_output(self) -> Path | None:
        default_output = self._default_output_file()
        dialog_options = {
            "title": "Salva file Excel",
            "defaultextension": ".xlsx",
            "filetypes": [("Excel Workbook", "*.xlsx")],
        }
        if default_output is not None:
            dialog_options["initialdir"] = str(default_output.parent)
            dialog_options["initialfile"] = default_output.name

        selected = filedialog.asksaveasfilename(
            **dialog_options,
        )
        if not selected:
            return None

        self.output_file = Path(selected)
        self.output_label.configure(text=f"Output: {self.output_file}")
        return self.output_file

    def convert(self) -> None:
        if not self.selected_files:
            messagebox.showwarning("Attenzione", "Seleziona almeno un file TXT o CSV.")
            return

        output_file = self.choose_output()
        if output_file is None:
            self.status_label.configure(text="Conversione annullata.", fg="red")
            return

        try:
            convert_files_to_excel(self.selected_files, output_file)
        except Exception as exc:  # noqa: BLE001 - GUI surface for conversion errors
            messagebox.showerror("Errore", f"Conversione fallita: {exc}")
            self.status_label.configure(text="", fg="red")
            return

        self.status_label.configure(text=f"File creato: {output_file}", fg="green")
        messagebox.showinfo("Completato", f"Conversione terminata.\n{output_file}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Converte file TXT/CSV con date USA in un file Excel .xlsx.",
    )
    parser.add_argument(
        "--input",
        nargs="+",
        type=Path,
        help="Uno o piu file TXT/CSV da convertire.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Percorso del file Excel .xlsx da generare.",
    )

    args = parser.parse_args(argv)
    has_cli_args = args.input is not None or args.output is not None
    if has_cli_args:
        if not args.input:
            parser.error("--input e obbligatorio quando usi la modalita CLI.")
        if args.output is None:
            parser.error("--output e obbligatorio quando usi la modalita CLI.")

    return args


def run_cli(input_files: list[Path], output_file: Path) -> int:
    try:
        convert_files_to_excel(input_files, output_file)
    except Exception as exc:  # noqa: BLE001 - CLI surface for conversion errors
        print(f"Conversione fallita: {exc}", file=sys.stderr)
        return 1

    print(f"File creato: {output_file}")
    return 0


def launch_gui() -> int:
    root = tk.Tk()
    DateConverterApp(root)
    root.mainloop()
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.input is not None:
        return run_cli(args.input, args.output)

    return launch_gui()


if __name__ == "__main__":
    raise SystemExit(main())
