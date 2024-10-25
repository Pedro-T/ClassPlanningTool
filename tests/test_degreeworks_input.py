import unittest
from pathlib import Path
from class_planning_tool.input_data import degreeworks_parser


class TestDegreeWorksInput(unittest.TestCase):

    def setUp(self):
        self.resource_path: Path = Path("./tests/resources")

        # mocking the input with a slightly stripped down & redacted version of extracted text
        # this is functionally the same as calling process_content(extract_text(open_file(file_path)))
        
        with open(self.resource_path / "test_pdf_content1.txt", "r") as f:
            self.results, self.free_classes = degreeworks_parser.process_content(f.read())

    def test_num_results(self):
        self.assertEqual(11, len(self.results))
    
    def test_incomplete_courses(self):
        expected_result: list[str] = ["CPSC 6000", "CPSC 6127", "CPSC 6179", "CPSC 6109"]
        for result in expected_result:
            self.assertTrue(result in self.results)
            self.assertDictEqual({"status": "incomplete", "term": ""}, self.results[result])

    def test_complete_courses(self):
        expected_result: dict[str, dict[str, str]] = {
            "CPSC 6119": {
                "status": "complete",
                "term": "FA23"
            },
            "CYBR 6126": {
                "status": "complete",
                "term": "SU23"
            },
            "CPSC 6185": {
                "status": "complete",
                "term": "SP24"
            },
            "CYBR 6136": {
                "status": "complete",
                "term": "SU24"
            },
            "CPSC 6175": {
                "status": "complete",
                "term": "SP24"
            },
        }
        self.assertDictEqual(expected_result, {key: self.results[key] for key in expected_result.keys()})

    def test_in_progress_courses(self):
        expected_result: dict[str, dict[str, str]] = {
            "CPSC 6125": {
                "status": "current",
                "term": "FA24"
            },
            "CPSC 6177": {
                "status": "current",
                "term": "FA24"
            }
        }
        self.assertDictEqual(expected_result, {key: self.results[key] for key in expected_result.keys()})
