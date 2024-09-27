import unittest
from unittest.mock import patch, MagicMock

from class_planning_tool.input_data.prereq_scraper import get_prerequisites, retrieve, parse_prereq_block, extract_information

class TestClassScheduleParsing(unittest.TestCase):


    def setUp(self) -> None:
        self.req_patcher = patch("urllib.request.urlopen")
        self.mock_urlopen: MagicMock = self.req_patcher.start()
        with open("tests/resources/course_descriptions_trimmed.html", "r") as f:
            self.mock_html = f.read()
        
        mock_resp: MagicMock = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = self.mock_html.encode('utf-8')
        self.mock_urlopen.return_value = mock_resp
    
    def tearDown(self):
        self.req_patcher.stop()

    def test_preqeq_parsing_single(self):
        block: str = "CPSC 1301K with a minimum grade of C"
        results: list[list[str]] = parse_prereq_block(block)
        self.assertListEqual([["CPSC 1301K"]], results)
    
    def test_prereq_parsing_alternates(self):
        block: str = "CPSC 1301 with a minimum grade of C or CPSC 1301H with a minimum grade of C or CPSC 1301K with a minimum grade of C or CPSC 1301I with a minimum grade of C"
        results: list[list[str]] = parse_prereq_block(block)
        self.assertListEqual([["CPSC 1301", "CPSC 1301H", "CPSC 1301K", "CPSC 1301I"]], results)
    
    def test_prereq_parsing_multi_group_complex(self):
        block: str = "CPSC 1301 with a minimum grade of C or CPSC 1301H with a minimum grade of C or CPSC 1301K with a minimum grade of C or CPSC 1301I with a minimum grade of C and CPSC 6677 or CPSC 9999 and CPSC 5555R"
        results: list[list[str]] = parse_prereq_block(block)
        self.assertListEqual([
                ["CPSC 1301", "CPSC 1301H", "CPSC 1301K", "CPSC 1301I"],
                ["CPSC 6677", "CPSC 9999"],
                ["CPSC 5555R"]
            ], results)


    @unittest.skip("Full end to end test with real query site, only execute this when necessary.")
    def test_end_to_end(self):
        pass