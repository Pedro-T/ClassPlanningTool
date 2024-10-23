import logging
from collections import defaultdict, deque

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='course_scheduler.log',
    filemode='w'
)
logger = logging.getLogger(__name__)

class CourseScheduler:
    def __init__(self, get_prerequisites, get_course_progress, get_offerings):
        """
        Initializes the scheduler with functions to fetch prerequisites, course progress, and offerings.

        :param get_prerequisites: Function returning dict[str, list[list[str]]]
        :param get_course_progress: Function returning dict[str, dict[str, str]]
        :param get_offerings: Function returning dict[str, list[str]]
        """
        # Fetch data via function calls
        self.prerequisites = get_prerequisites()
        self.course_progress = get_course_progress()
        self.offerings = get_offerings()

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
            if semester in self.offerings.get(course, [])
        ]
        logger.info(f"Available courses in {semester}: {available}")
        return available

    def find_best_schedule(self, max_courses_per_semester=8):
        """Attempts to create the best schedule to complete all required courses."""
        semesters = [
            "FA24", "SP25", "SU25", "FA25", "SP26", "SU26",
            "FA26", "SP27", "SU27", "FA27"
        ]

        schedule = []
        remaining_courses = set(self.required_courses)
        sorted_courses = self.topological_sort()

        for semester in semesters:
            available_courses = self.available_courses_in_semester(semester, remaining_courses)
            semester_courses = []

            for course in sorted_courses:
                if course in available_courses and len(semester_courses) < max_courses_per_semester:
                    semester_courses.append(course)
                    remaining_courses.remove(course)

            if semester_courses:
                schedule.append((semester, semester_courses))
            if not remaining_courses:
                break

        if remaining_courses:
            logger.warning(f"Unable to complete all required courses. Remaining: {remaining_courses}")

        return schedule

    def print_schedule(self, schedule):
        """Prints the schedule in a user-friendly format."""
        for semester, courses in schedule:
            logger.info(f"{semester}: {', '.join(courses)}")

def get_prerequisites():
    """
    Returns a dictionary representing the prerequisites of courses.
    Courses may require one or more prerequisites in groups.
    """
    return {
        "CPSC 5555": [["CPSC 1111"], ["CPSC 2222", "CPSC 3333"]],
        "CPSC 6666": [["CPSC 5555"]],
        "MATH101": [],
        "CPSC 2222": [["MATH101"]],
        "CPSC 3333": [["MATH101"]],
    }

def get_course_progress():
    """
    Returns a dictionary with course progress, showing the completion status of courses.
    Courses with 'complete' status are ignored in scheduling.
    """
    return {
        "CPSC 1111": {"status": "complete", "term": "SU24"},
        "CPSC 2222": {"status": "in_progress", "term": "FA24"},
        "CPSC 3333": {"status": "incomplete", "term": ""},
        "CPSC 5555": {"status": "incomplete", "term": ""},
        "CPSC 6666": {"status": "incomplete", "term": ""},
        "MATH101": {"status": "incomplete", "term": ""}
    }

def get_offerings():
    """
    Returns a dictionary representing the available semesters for each course.
    """
    return {
        "CPSC 1111": ["SP24", "SU24"],
        "CPSC 2222": ["FA24", "SP25"],
        "CPSC 3333": ["FA24", "SP25"],
        "CPSC 5555": ["FA24", "SP25"],
        "CPSC 6666": ["SP25", "FA25"],
        "MATH101": ["SP24", "SU24", "FA24", "SP25"]
    }
