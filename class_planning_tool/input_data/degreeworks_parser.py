import fitz
from re import Pattern, compile

COURSE_CODE: Pattern = compile(r"^[A-Z]{4} \d{4}")

COMPLETED_COURSE: Pattern = compile(r"([A-Z]{4} \d{4}) ?\n.{0,100}\n[ABCDF] ?\n\d{1} ?\n(Summer|Fall|Spring) (20\d{2})")

class DegreeWorksParsingError(Exception):
    """
    Wrapper class for exceptions triggered during DegreeWorks PDF parsing. Provides a general message and access to the underlying exception.
    """
    def __init__(self, message: str, exception: Exception):
        super().__init__(message)
        self.message: str = message
        self.exception: Exception = exception
    
    def __str__(self) -> str:
        return f"Unable to process PDF. {self.message}. Caused by {repr(self.exception)}"


def open_file(file_path: str) -> fitz.Document:
    try:
        return fitz.Document(file_path)
    except (TypeError, FileNotFoundError, fitz.FileDataError, fitz.EmptyFileError, ValueError) as e:
        raise DegreeWorksParsingError("Could not open or read PDF file", e)


def process_content(text: str) -> dict[str, dict[str, str]]:
    results: dict[str, dict[str, str]] = {}

    completed_courses: list[tuple[str, str, str]] = COMPLETED_COURSE.findall(text)
    for course in completed_courses:
        results[course[0]] = {
            "status": "complete",
            "term": f"{course[1][:2].upper()}{course[2][2:]}"
        }

    # TODO incomplete courses

    # TODO in progress courses

    return results



def parse_pdf(file_path: str) -> dict[str, dict[str, str]]:
    """
    Open a PDF, extract course completion data, and return a dictionary representing the student's course progress.
    
    Args:
        file_path (str): path to the PDF to open
    
    Returns:
        dict[str, dict[str, str]]: dictionary representing course progress.
    
    Raises:
        DegreeWorksParsingError: wrapper for several errors from various functions
        
    An example of the progress map structure is

    "CPSC 1111": {
        "status": "complete",
        "term": "SU24"
    },
    "CPSC 2222": {
        "status": "in_progress",
        "term": "FA24"
    },
    "CPSC 3333": {
        "status": "incomplete",
        "term": ""
    }
    
    """
    doc: fitz.Document = open_file(file_path)
    text: str = "\n".join([doc.load_page(i).get_textpage().extractText()[2:] for i in range(len(doc))]) # reason for excluding first two lines is the header
    return process_content(text)
    