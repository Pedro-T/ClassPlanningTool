
from collections import defaultdict, deque, OrderedDict

# Configure the logger
import os
import logging

# Redirect log file to the user's home directory
user_home = os.path.expanduser("~")
log_file_path = os.path.join(user_home, "course_scheduler.log")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file_path,
    filemode='w'
)

logger = logging.getLogger(__name__)
class Planner:
    def __init__(self, course_progress, free_electives, course_schedule, prerequisites, titles: dict[str, str]):
        
        """Initializes the scheduler with prerequisites of the degree being pursued,
        course progress information obtained from degreeworks,
        and the semesters that each course is offered (offerings)."""
        self.prerequisites = prerequisites
        self.course_progress = course_progress
        self.offerings = course_schedule
        self.titles: dict[str, str] = titles
        self.free_electives = free_electives

        # Identify required courses based on progress (ignore completed courses)
        self.required_courses = self.get_remaining_courses()

        # Build the course graph and calculate in-degrees
        self.course_graph = self.build_course_graph(self.prerequisites)
        self.in_degree = self.calculate_in_degrees(self.course_graph)

    def get_remaining_courses(self):
        """Determines which courses are still required by filtering out completed ones."""
        remaining = {
            course for course, progress in self.course_progress.items()
            if progress["status"] != "complete"
        }
        logger.info(f"Remaining courses: {remaining}")
        return remaining

    def build_course_graph(self, prerequisites):
        """Creates a directed graph from the prerequisites data."""
        graph = defaultdict(list)

        for course in self.required_courses:
            graph[course]  # Initialize all required courses in the graph

        for course, prereq_groups in prerequisites.items():
            for prereq_group in prereq_groups:
                for prereq in prereq_group:
                    graph[prereq].append(course)

        logger.debug(f"Built course graph: {graph}")
        return graph

    def calculate_in_degrees(self, graph):
        """Calculates the in-degrees for all nodes in the graph."""
        in_degree = defaultdict(int)

        for course in graph:
            in_degree[course] = 0

        for prereq in graph:
            for dependent_course in graph[prereq]:
                in_degree[dependent_course] += 1

        logger.debug(f"Calculated in-degrees: {in_degree}")
        return in_degree

    def topological_sort(self):
        """Performs a topological sort on the course graph."""
        zero_in_degree = deque(
            [course for course in self.course_graph if self.in_degree[course] == 0]
        )
        sorted_courses = []

        while zero_in_degree:
            course = zero_in_degree.popleft()
            logger.info(f"Processing course: {course}")
            sorted_courses.append(course)

            for dependent_course in self.course_graph[course]:
                self.in_degree[dependent_course] -= 1
                if self.in_degree[dependent_course] == 0:
                    zero_in_degree.append(dependent_course)

        logger.debug(f"Final sorted courses: {sorted_courses}")
        return sorted_courses

    def available_courses_in_semester(self, semester, remaining_courses):
        """Returns a list of courses available in a given semester."""
        available = [
            course for course in remaining_courses
            if semester in self.offerings.get(course, []) and course != "CPSC 6000"
        ]
        logger.info(f"Available courses in {semester}: {available}")
        return available

    def find_best_schedule(self, max_courses_per_semester=4) -> dict[str, list[dict[str, str]]]:
        """Attempts to create the best schedule to complete all required courses."""
        semesters = [
            "FA24", "SP25", "SU25", "FA25", "SP26", "SU26",
            "FA26", "SP27", "SU27", "FA27", "SP28", "SU28", 
            "FA28", "SP29", "SU29", "FA29"
        ]

        # Initialize the schedule as a dictionary with semesters as keys
        schedule = OrderedDict()
        remaining_courses = set(self.required_courses)
        sorted_courses = self.topological_sort()

        # Filter out invalid electives
        invalid_electives = {"6103", "6105", "6106"}
        valid_electives = [
            course for course in self.required_courses
            if course.startswith("6") and course not in invalid_electives
        ]

        # Track each semester where courses are added
        final_semester = None  # Initialize the final_semester variable

        for semester in semesters:
            available_courses = self.available_courses_in_semester(semester, remaining_courses)
            semester_courses = []

            for course in sorted_courses:
                if course in available_courses and len(semester_courses) < max_courses_per_semester:
                    semester_courses.append({"code": course, "title": self.titles[course]})
                    remaining_courses.remove(course)

            if semester_courses:
                schedule[semester] = semester_courses
                final_semester = semester  # Update final_semester to the latest one with courses
                logger.debug(f"Updated final_semester to: {final_semester}")

            if not remaining_courses:
                break

        # Ensure 'CPSC 6000' is placed in the final semester
        logger.debug(f"Final semester before placing CPSC 6000: {final_semester}")
        # Ensure 'CPSC 6000' is placed in the final semester
        logger.debug(f"Remaining courses before placing CPSC 6000: {remaining_courses}")
        if "CPSC 6000" in remaining_courses:
            if final_semester not in schedule:
                schedule[final_semester] = []
            schedule[final_semester].append({"code": "CPSC 6000", "title": self.titles["CPSC 6000"]})
            remaining_courses.remove("CPSC 6000")
            logger.info(f"CPSC 6000 added to final semester: {final_semester}")
        else:
            logger.warning(f"CPSC 6000 not found in remaining_courses!")

        # Add valid electives to fill free elective spots
        elective_count = min(self.free_electives, len(valid_electives))
        elective_courses = valid_electives[:elective_count]

        for course in elective_courses:
            # Add elective courses to the earliest available semester with space
            for semester in semesters:
                if len(schedule.get(semester, [])) < max_courses_per_semester:
                    if semester not in schedule:
                        schedule[semester] = []
                    schedule[semester].append({"code": course, "title": self.titles[course]})
                    break

        # Quick fix for three-semester blocks
        length = len(list(schedule.keys())) % 3
        if length:
            last_year = list(schedule.keys())[-1][2:]
            if length == 1:
                schedule[f"SU{last_year}"] = []
            schedule[f"FA{last_year}"] = []

        if remaining_courses:
            logger.warning(f"Unable to complete all required courses. Remaining: {remaining_courses}")

        self.print_schedule(schedule)
        return schedule

    def print_schedule(self, schedule: dict[str, list[dict[str, str]]]):
        """Prints the schedule in a user-friendly format."""
        for semester, courses in schedule.items():
            course_names = [course["code"] for course in courses]
            logger.info(f"{semester}: {', '.join(course_names)}")
