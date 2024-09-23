from pathlib import Path

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

from collections import OrderedDict

_TITLE_FONT: Font = Font(name="Helvetica", size=24)
_VALUE_FONT: Font = Font(name="Helvetica", size=11)
_VALUE_FONT_BOLD: Font = Font(name="Helvetica", bold=True, size=11)
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

def write_semester_block(sheet: Worksheet, row_start: int, column_start: int, semester: str, courses: list[dict[str, str]]) -> None:
    """
    Write the block for one semester, which is a simple three column area of code | title | credits
    Header is semester name
    Last row is a total credit count
    Maximum length in courses defined in _SEMESTER_CAPACITY

    Args:
        sheet (Worksheet)               : the sheet to modify
        row_start (int)                 : row offset from the top where this block starts
        column_start (int)              : column offset from the left where this block starts
        courses (list[dict[str, str]])   : list of courses to include
    """

    # semester name
    sheet.merge_cells(start_row=row_start, start_column=column_start, end_row=row_start, end_column=column_start+2)
    header: Cell = sheet.cell(row_start, column_start)
    header.value = semester
    header.font = _VALUE_FONT_BOLD
    header.alignment = _CENTER_ALIGNMENT

    # course list
    detail_order: tuple[str] = ("code", "title", "description")
    fonts_order: tuple[str] = (_VALUE_FONT_BOLD, _VALUE_FONT, _VALUE_FONT)
    for course_idx, course in enumerate(courses):
        for col_idx_offset in range(len(detail_order)):
            cell: Cell = sheet.cell(row_start+course_idx+1, column_start+col_idx_offset+1)
            cell.value = course[detail_order]
            cell.font = fonts_order[col_idx_offset]
            cell.alignment = _CENTER_ALIGNMENT
    
    # course count

    sheet.merge_cells(start_row=row_start+_SEMESTER_CAPACITY+1, start_column=column_start, end_row=row_start+_SEMESTER_CAPACITY+1, end_column=column_start+2)
    footer: Cell = sheet.cell(row_start+_SEMESTER_CAPACITY+1, column_start)
    footer.value = f"Courses: {len(courses)}"
    footer.font = _VALUE_FONT_BOLD
    footer.alignment = _CENTER_ALIGNMENT


def write_year_block(semesters: list[dict[str, str]]) -> None:
    pass


def write_plan_workbook(course_plan: OrderedDict[str, list[dict[str, str]]]) -> None:
    """
    Write the supplied study plan to an Excel sheet.

    Args:
        course_plan (OrderedDict[str, list[dict[str, str]]]): course plan to export
    
    Semester keys must be of the form (season) (year), written as "Spring 2024". Each semester key can have up to four course info dictionaries. Example course info:
        "code": "CPSC6136",
        "title": "Human Aspects of Cybersecurity",
        "description": "This course examines tawhe human......"

    """
    pass