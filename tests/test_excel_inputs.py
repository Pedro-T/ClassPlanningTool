import unittest
from class_planning_tool.input_data.excel_inputs import get_cutoff_format, populate_column_semester_map


class TestClassScheduleParsing(unittest.TestCase):

    def test_semester_cutoff_formatter_valid(self):
        self.assertEqual(241, get_cutoff_format("SP24"))
        self.assertEqual(313, get_cutoff_format("FA31"))
        self.assertEqual(252, get_cutoff_format("SU25"))
    
    def test_semester_cutoff_formatter_invalid(self):
        with self.assertRaises(ValueError):
            get_cutoff_format("AA25")
        with self.assertRaises(ValueError):
            get_cutoff_format("FAA6")
        with self.assertRaises(ValueError):
            get_cutoff_format("SU5")
        
    def test_semester_index_map_valid_no_cutoff(self):
        row: list[str] = ["Course", "Course Title", "SP20", "SU20", "FA20"]
        expectation: dict[int, str] = {
            "SP20": 2,
            "SU20": 3,
            "FA20": 4
        }
        self.assertDictEqual(expectation, populate_column_semester_map(row))

    def test_semester_index_map_invalid(self):
        row: list[str] = ["Course", "Course Title", "ABCD", "NONSENSE"]
        self.assertFalse(populate_column_semester_map(row))
    

    def test_semester_index_map_valid_with_cutoff(self):
        row: list[str] = ["Course", "Course Title", "SP20", "SU20", "FA20", "SP21", "SU21", "FA21"]
        cutoff: str = "FA20"
        expectation: dict[int, str] = {
            "FA20": 4,
            "SP21": 5,
            "SU21": 6,
            "FA21": 7
        }
        self.assertDictEqual(expectation, populate_column_semester_map(row, cutoff))
    
