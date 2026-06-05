from __future__ import annotations

import csv
import re
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape

USA_DATETIME_FORMAT = "%m/%d/%Y %H:%M:%S"
ITA_DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
INVALID_SHEET_CHARS = re.compile(r"[\[\]\*:/\\?]")


def convert_date_string(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        return value

    try:
        parsed = datetime.strptime(stripped, USA_DATETIME_FORMAT)
    except ValueError:
        return value

    return parsed.strftime(ITA_DATETIME_FORMAT)


def read_delimited_file(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel

        rows = []
        reader = csv.reader(handle, dialect)
        for row in reader:
            rows.append([convert_date_string(cell) for cell in row])
        return rows


def sanitize_sheet_name(name: str, fallback_index: int) -> str:
    cleaned = INVALID_SHEET_CHARS.sub("_", name).strip()
    cleaned = cleaned[:31] if cleaned else f"Sheet{fallback_index}"
    return cleaned or f"Sheet{fallback_index}"


def ensure_unique_sheet_names(names: Iterable[str]) -> list[str]:
    result: list[str] = []
    used: set[str] = set()
    for index, base_name in enumerate(names, start=1):
        name = sanitize_sheet_name(base_name, index)
        if name not in used:
            used.add(name)
            result.append(name)
            continue

        counter = 1
        while True:
            suffix = f"_{counter}"
            candidate = f"{name[: 31 - len(suffix)]}{suffix}"
            if candidate not in used:
                used.add(candidate)
                result.append(candidate)
                break
            counter += 1
    return result


def _column_name(index: int) -> str:
    result = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def _sheet_xml(rows: list[list[str]]) -> str:
    xml_rows = []
    for row_index, row in enumerate(rows, start=1):
        cells = []
        for col_index, value in enumerate(row, start=1):
            cell_ref = f"{_column_name(col_index)}{row_index}"
            escaped_value = escape(value)
            cells.append(
                f'<c r="{cell_ref}" t="inlineStr"><is><t>{escaped_value}</t></is></c>'
            )
        xml_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(xml_rows)}</sheetData>'
        "</worksheet>"
    )


def write_xlsx(output_path: Path, sheets: list[tuple[str, list[list[str]]]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    workbook_sheets = "".join(
        f'<sheet name="{escape(name)}" sheetId="{index}" r:id="rId{index}"/>'
        for index, (name, _) in enumerate(sheets, start=1)
    )
    workbook_rels = "".join(
        f'<Relationship Id="rId{index}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
        f'Target="worksheets/sheet{index}.xml"/>'
        for index in range(1, len(sheets) + 1)
    )
    content_types_sheets = "".join(
        f'<Override PartName="/xl/worksheets/sheet{index}.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for index in range(1, len(sheets) + 1)
    )

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            (
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                '<Default Extension="rels" '
                'ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                '<Default Extension="xml" ContentType="application/xml"/>'
                f"{content_types_sheets}"
                '<Override PartName="/xl/workbook.xml" '
                'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                "</Types>"
            ),
        )
        archive.writestr(
            "_rels/.rels",
            (
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" '
                'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
                'Target="xl/workbook.xml"/>'
                "</Relationships>"
            ),
        )
        archive.writestr(
            "xl/workbook.xml",
            (
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                f"<sheets>{workbook_sheets}</sheets>"
                "</workbook>"
            ),
        )
        archive.writestr(
            "xl/_rels/workbook.xml.rels",
            (
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                f"{workbook_rels}"
                "</Relationships>"
            ),
        )
        for index, (_, rows) in enumerate(sheets, start=1):
            archive.writestr(f"xl/worksheets/sheet{index}.xml", _sheet_xml(rows))


def convert_files_to_excel(input_files: list[Path], output_file: Path) -> None:
    if not input_files:
        raise ValueError("Nessun file selezionato.")

    sheet_names = ensure_unique_sheet_names([file.stem for file in input_files])
    sheets_data: list[tuple[str, list[list[str]]]] = []
    for file_path, sheet_name in zip(input_files, sheet_names, strict=True):
        rows = read_delimited_file(file_path)
        sheets_data.append((sheet_name, rows))

    write_xlsx(output_file, sheets_data)
