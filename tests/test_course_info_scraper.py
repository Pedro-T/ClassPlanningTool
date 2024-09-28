import unittest

from bs4 import BeautifulSoup
from class_planning_tool.input_data.prereq_scraper import get_prerequisites, parse_prereq_block, extract_information

class TestClassScheduleParsing(unittest.TestCase):

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

    def test_extract_info_full(self):
        expected = {
            "CPSC 1111": [
                ["CPSC 1301K", "CPSC 1301", "CPSC 1301H", "CPSC 1301I", "CPSC 1301X"]
            ],
            "CPSC 2222": [
                ["CPSC 1301K"]
            ],
            "CPSC 3333": [],
            "CPSC 4444": [
                ["CPSC 1301K"],
                ["CPSC 7777"]
            ],
            "CPSC 5555": []
        }

        with open("tests/resources/course_descriptions_trimmed.html", "r") as f:
            soup: BeautifulSoup = BeautifulSoup(f.read(), "html.parser")
        results = extract_information(soup)
        self.assertDictEqual(expected, results)


    @unittest.skip("Full end to end test with real query to site, only execute this when necessary.")
    def test_end_to_end(self):
        """
        Due to the very long list on the actual page, this will only be a spot check for three randomly chosen courses.
        """
        pass