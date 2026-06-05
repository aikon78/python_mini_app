from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import app


class FakeListbox:
    def __init__(self, selection: tuple[int, ...]) -> None:
        self._selection = selection
        self.deleted: list[int] = []

    def curselection(self) -> tuple[int, ...]:
        return self._selection

    def delete(self, index: int) -> None:
        self.deleted.append(index)


class FakeLabel:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}

    def configure(self, **kwargs: str) -> None:
        self.values.update(kwargs)


class AppTests(unittest.TestCase):
    def test_main_cli_creates_output_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_file = tmp_path / "input.csv"
            output_file = tmp_path / "result.xlsx"
            input_file.write_text("name,date\nMario,7/1/2026 23:00:00\n", encoding="utf-8")

            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                exit_code = app.main(
                    ["--input", str(input_file), "--output", str(output_file)]
                )

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_file.exists())
            self.assertIn(str(output_file), stdout.getvalue())

    def test_main_cli_returns_error_code_for_missing_input_file(self) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            exit_code = app.main(
                ["--input", "missing.csv", "--output", "result.xlsx"]
            )

        self.assertEqual(exit_code, 1)
        self.assertIn("Conversione fallita", stderr.getvalue())

    def test_remove_selected_files_resets_output_when_list_becomes_empty(self) -> None:
        instance = app.DateConverterApp.__new__(app.DateConverterApp)
        instance.selected_files = [Path("first.csv")]
        instance.output_file = Path("out.xlsx")
        instance.file_listbox = FakeListbox((0,))
        instance.output_label = FakeLabel()
        instance.status_label = FakeLabel()

        app.DateConverterApp.remove_selected_files(instance)

        self.assertEqual(instance.selected_files, [])
        self.assertIsNone(instance.output_file)
        self.assertEqual(instance.output_label.values["text"], "Output: non selezionato")
        self.assertEqual(instance.status_label.values["text"], "")


if __name__ == "__main__":
    unittest.main()