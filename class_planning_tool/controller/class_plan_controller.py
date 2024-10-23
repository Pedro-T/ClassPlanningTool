


from input_data.degreeworks_parser import parse_pdf

from input_data.excel_inputs import get_class_schedule_data

from input_data.prereq_scraper import get_prerequisites

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
        Process the 4-year schedule Excel file.
        Args:
            schedule_file (str): Path to the Excel file.
            start_semester (str): Optional cutoff starting semester in 'SP24' format.
        
        Returns:
            dict: The schedule data as a dictionary.
        """
        try:
           
            schedule_data = get_class_schedule_data(schedule_file, start_semester)
            return schedule_data
        except Exception as e:
            return str(e) 
        
    def process_prerequisites(self, url):
        """
        Scrape the prerequisites for courses from a given URL.
        Args:
            url (str): The URL to scrape for course prerequisites.
        
        Returns:
            dict: A dictionary mapping course codes to prerequisites.
        """
        try:
            
            prereq_data = get_prerequisites(url)
            return prereq_data
        except Exception as e:
            return str(e) 