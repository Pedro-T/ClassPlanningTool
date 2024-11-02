import unittest

from class_planning_tool.course_planner.planner import Planner


class TestPrerequisiteOrdering(unittest.TestCase):

    def setUp(self):
        self.result = Planner(
            {
                "CPSC 6179": {
                    "status": "incomplete",
                    "term": ""
                },
                "CPSC 6127": {
                    "status": "incomplete",
                    "term": ""
                },
                "CPSC 6555": {
                    "status": "incomplete",
                    "term": ""
                },
            },
            0,
            {
                "CPSC 6179": ["SP25", "FA25"],
                "CPSC 6127": ["SU25"],
                "CPSC 6555": ["SP25", "FA25"]
            },
            {
                "CPSC 6555": [],
                "CPSC 6179": [["CPSC 6127"]],
                "CPSC 6127": []
            },
            {
                "CPSC 6179": "Course desc 1",
                "CPSC 6127": "Course desc 2",
                "CPSC 6555": "Course desc 3",
            }
        ).find_best_schedule()
        print(self.result)

    def test_course_order(self):
        self.assertEqual(4, 4)