from pathlib import Path

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

from collections import OrderedDict

_TITLE_FONT: Font = Font(name="Helvetica", size=24)
_VALUE_FONT: Font = Font(name="Helvetica", size=11)
_CENTER_ALIGNMENT: Alignment = Alignment(horizontal="center", vertical="center")
_SEMESTER_CAPACITY: int = 4

_COLUMN_WIDTHS: dict[str, int] = {
    "A": 10,
    "B": 30,
    "C": 30,
    "D": 30
}

def write_header(sheet: Worksheet) -> None:
    """
    Writes the centered title for the table

    Args:
        sheet (Worksheet): the sheet to modify
    """
    sheet.merge_cells("A2:A4")
    title_cell: Cell = sheet["A2"]
    title_cell.value = "Study Plan"
    title_cell.font = _TITLE_FONT
    title_cell.alignment = _CENTER_ALIGNMENT

def format_sheet(sheet: Worksheet) -> None:
    """
    Sets the column widths for the sheet based on _COLUMN_WIDTHS

    Args:
        sheet (Worksheet)   : the sheet to modify
    """
    for column_letter, width in _COLUMN_WIDTHS.items():
        sheet.column_dimensions[column_letter].width = width

def write_semester_block(sheet: Worksheet, row_start: int, column_start: int, semester: str, courses: list[dict[str|int]]) -> None:
    """
    Write the block for one semester, which is a simple three column area of code | title | credits
    Header is semester name
    Last row is a total credit count
    Maximum length in courses defined in _SEMESTER_CAPACITY

    Args:
        sheet (Worksheet)               : the sheet to modify
        row_start (int)                 : row offset from the top where this block starts
        column_start (int)              : column offset from the left where this block starts
        courses (list[dict[str|int]])   : list of courses to include
    """
    pass

def write_year_block() -> None:
    pass


def write_plan_workbook(course_plan: OrderedDict[str, list[dict[str, str|int]]]) -> None:
    """
    Write the supplied study plan to an Excel sheet.

    Args:
        course_plan (OrderedDict[str, list[dict[str, str|int]]]): course plan to export
    
    Semester keys must be of the form (season) (year), written as "Spring 2024". Each semester key can have up to four course info dictionaries. Example course info:
        "code": "CPSC6136",
        "title": "Human Aspects of Cybersecurity",
        "description": "This course examines tawhe human......",
        "credits": 3

    """
    pass