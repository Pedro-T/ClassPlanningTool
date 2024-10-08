import fitz

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
    pass