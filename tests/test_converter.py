from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from converter import (
    convert_date_string,
    convert_files_to_excel,
    ensure_unique_sheet_names,
)


class ConverterTests(unittest.TestCase):
    def test_convert_date_string_from_usa_to_italian_format(self) -> None:
        self.assertEqual(
            convert_date_string("7/1/2026 23:00:00"),
            "01/07/2026 23:00:00",
        )

    def test_convert_date_string_leaves_non_dates_unchanged(self) -> None:
        self.assertEqual(convert_date_string("not-a-date"), "not-a-date")

    def test_convert_files_to_excel_creates_xlsx_with_converted_data(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            csv_file = tmp_path / "input.csv"
            txt_file = tmp_path / "input_2.txt"
            output_file = tmp_path / "out.xlsx"

            csv_file.write_text(
                "name,date\nMario,7/1/2026 23:00:00\n",
                encoding="utf-8",
            )
            txt_file.write_text(
                "col1;col2\nA;12/31/2026 01:02:03\n",
                encoding="utf-8",
            )

            convert_files_to_excel([csv_file, txt_file], output_file)

            self.assertTrue(output_file.exists())
            with zipfile.ZipFile(output_file) as archive:
                sheet1 = archive.read("xl/worksheets/sheet1.xml").decode("utf-8")
                sheet2 = archive.read("xl/worksheets/sheet2.xml").decode("utf-8")

            self.assertIn("01/07/2026 23:00:00", sheet1)
            self.assertIn("31/12/2026 01:02:03", sheet2)

    def test_ensure_unique_sheet_names_handles_case_insensitive_collisions(self) -> None:
        names = ensure_unique_sheet_names(["Report", "report", "REPORT"])
        self.assertEqual(names, ["Report", "report_1", "REPORT_2"])


if __name__ == "__main__":
    unittest.main()
