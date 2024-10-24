
from collections import OrderedDict

from input_data.degreeworks_parser import parse_pdf

from input_data.excel_inputs import get_class_schedule_data

from input_data.prereq_scraper import get_prerequisites

from output_generation.class_plan_writer import write_plan_workbook

from logic_behind_sorting_courses.planner import Planner

class ClassPlanController:
    def __init__(self):
        pass 

    def process_degreeworks_file(self, degree_file):
        try:

            degree_data = parse_pdf(degree_file)


            return degree_data

        except Exception as e:
            return str(e)
    def process_schedule_file(self, schedule_file, start_semester=""):
        """
        Wrapper for prerequisite schedule file parser call
        """
        try:
           
            schedule_data = get_class_schedule_data(schedule_file, start_semester)
            return schedule_data
        except Exception as e:
            return str(e) 
        
    def process_prerequisites(self, url):
        """
        Wrapper for prerequisite input handler call
        """
        try:
            
            prereq_data = get_prerequisites(url)
            return prereq_data
        except Exception as e:
            return str(e) 
    
    def get_plan(self, degree_data, schedule_data, prereq_data):
        """Wrapper for retrieving course plan based on inputs"""
        try:
            return Planner(degree_data, schedule_data, prereq_data).find_best_schedule()
        except Exception as e:
            return str(e)
    
    def generate_course_plan(self, course_plan):
        """
        Wrapper for call to Excel writer
        """

        try:
            # Use the write_plan_workbook to generate the file
            write_plan_workbook(course_plan)
        except Exception as e:
            print(f"Failed to generate Excel file: {e}")