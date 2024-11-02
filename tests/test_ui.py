import unittest
import sys
import os
import re  
from unittest.mock import patch, MagicMock


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from class_planning_tool.ui.dashboard import Dashboard
import tkinter as tk

class TestDashboard(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.dashboard = Dashboard(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_upload_degree_file_valid(self):
        with patch('tkinter.filedialog.askopenfilename', return_value="test_file.pdf"):
            with patch('class_planning_tool.ui.dashboard.check_file_type', return_value=True):
                mock_button = MagicMock()
                mock_button.filename_label = MagicMock()
                self.dashboard.upload_degree_file(mock_button)
                self.assertEqual(self.dashboard.degree_file_path, "test_file.pdf")

    def test_upload_degree_file_invalid(self):
        with patch('tkinter.filedialog.askopenfilename', return_value="test_file.txt"):
            with patch('class_planning_tool.ui.dashboard.check_file_type', return_value=False):
                mock_button = MagicMock()
                mock_button.filename_label = MagicMock()
                self.dashboard.upload_degree_file(mock_button)
                self.assertIsNone(self.dashboard.degree_file_path)

    def test_upload_schedule_file_valid(self):
        with patch('tkinter.filedialog.askopenfilename', return_value="schedule.xlsx"):
            with patch('class_planning_tool.ui.dashboard.check_file_type', return_value=True):
                mock_button = MagicMock()
                mock_button.filename_label = MagicMock()
                self.dashboard.upload_schedule_file(mock_button)
                self.assertEqual(self.dashboard.schedule_file_path, "schedule.xlsx")

    def test_upload_schedule_file_invalid(self):
        with patch('tkinter.filedialog.askopenfilename', return_value="schedule.docx"):
            with patch('class_planning_tool.ui.dashboard.check_file_type', return_value=False):
                mock_button = MagicMock()
                mock_button.filename_label = MagicMock()
                self.dashboard.upload_schedule_file(mock_button)
                self.assertIsNone(self.dashboard.schedule_file_path)

    def test_update_status(self):
        self.dashboard.degree_file_path = "degree.pdf"
        self.dashboard.schedule_file_path = "schedule.xlsx"
        self.dashboard.update_status()
        self.assertIn("✅", self.dashboard.status_box.get("1.0", "end"))

    def test_process_files(self):


        self.dashboard.controller.process_degreeworks_file = MagicMock(return_value=({}, 5)) 
        self.dashboard.controller.process_schedule_file = MagicMock(return_value={})
        self.dashboard.controller.process_prerequisites = MagicMock(return_value=({}, {}))
        
        loading_window = tk.Toplevel(self.root)
        self.dashboard.process_files(loading_window)

        self.assertIsInstance(self.dashboard.course_plan, dict)

    def test_download_result(self):
        self.dashboard.course_plan = {"Fall 2024": [{"code": "CS101", "title": "Intro to Computer Science"}]}
        with patch('tkinter.messagebox.showinfo') as mock_info, patch('os.startfile') as mock_startfile, patch.object(self.dashboard.controller, 'generate_course_plan', return_value=True):
            self.dashboard.download_result()
            mock_info.assert_called_once_with("Success", "Your result Excel file has been created: Course_Plan.xlsx", parent=self.dashboard.root)
            mock_startfile.assert_called_once_with("Course_Plan.xlsx")

    def test_url_validation(self):
        # Test a valid URL
        valid_url = "https://example.com/path"
        self.dashboard.url_entry.insert(0, valid_url)
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.dashboard.submit_files()
            mock_error.assert_not_called()  # No error for valid URL

        # Clear entry field for the next test
        self.dashboard.url_entry.delete(0, 'end')

        # Test an invalid URL
        invalid_url = "htp:/invalid-url"
        self.dashboard.url_entry.insert(0, invalid_url)
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.dashboard.submit_files()
            mock_error.assert_called_once_with("Invalid URL", "Please enter a valid URL.", parent=self.dashboard.root)

        # Clear entry field after the test
        self.dashboard.url_entry.delete(0, 'end')
if __name__ == "__main__":
    unittest.main(verbosity=2)
