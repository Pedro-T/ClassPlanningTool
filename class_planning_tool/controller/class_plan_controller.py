from class_planning_tool.input_data.degreeworks_parser import parse_pdf
from class_planning_tool.input_data.excel_inputs import get_class_schedule_data
from class_planning_tool.input_data.prereq_scraper import Scraper
from class_planning_tool.output_generation.class_plan_writer import write_plan_workbook
from class_planning_tool.course_planner.planner import Planner


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
        scraper: Scraper = Scraper(url)
        return scraper.get_prerequisites(), scraper.title_map
    
    def get_plan(self, degree_data, free_electives, schedule_data, prereq_data, title_map):
        """Wrapper for retrieving course plan based on inputs"""
        return Planner(degree_data, free_electives, schedule_data, prereq_data, title_map).find_best_schedule()
    
    def generate_course_plan(self, course_plan):
        """
        Wrapper for call to Excel writer
        """
        write_plan_workbook(course_plan)