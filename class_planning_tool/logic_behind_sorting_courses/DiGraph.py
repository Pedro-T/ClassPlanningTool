import collections
import json
import os

class DiGraph:
    def __init__(self):
        # Adjacency list representation
        self.graph = collections.defaultdict(list)
        self.vertices = set()

    def add_course(self, prerequisite, course):
        """Adds a course and its prerequisite to the graph."""
        if prerequisite != "NONE":
            self.vertices.add(prerequisite)
            self.graph[prerequisite].append(course)

        # Add the course even if it has no prerequisite
        self.vertices.add(course)
        self.graph[course]  # Ensure the course is in the graph

    def remove_course(self, course):
        """Removes a course from the graph along with its dependencies."""
        self.graph.pop(course, None)  # Remove as key

        # Remove from all adjacency lists
        for neighbors in self.graph.values():
            if course in neighbors:
                neighbors.remove(course)

        self.vertices.discard(course)
        print(f"{course} has been removed.")

    def print_course_info(self, course):
        """Prints course information, including its prerequisites."""
        course = course.strip()
        if course in self.graph:
            print(f"{course} prerequisites: {self.graph[course]}")
        else:
            print(f"{course} does not exist in the graph.")

    def topological_sort(self):
        """Performs topological sorting to determine course order."""
        in_degree = {v: 0 for v in self.vertices}

        # Calculate in-degrees
        for course, neighbors in self.graph.items():
            for neighbor in neighbors:
                in_degree[neighbor] += 1

        # Queue for courses with no prerequisites
        queue = collections.deque([v for v in in_degree if in_degree[v] == 0])
        sorted_order = []

        while queue:
            course = queue.popleft()
            sorted_order.append(course)

            for neighbor in self.graph[course]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_order) != len(self.vertices):
            print("There exists a cycle in the graph, topological sort not possible.")
            return []

        return sorted_order

    def load_courses_from_file(self, filename):
        """Loads courses and their prerequisites from a .txt file."""
        with open(filename, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) == 2:
                    prerequisite, course = parts
                    self.add_course(prerequisite.strip(), course.strip())

    def load_test_cases(self):
        """Loads predefined test cases."""
        self.add_course("NONE", "BIOL_1001")
        self.add_course("NONE", "BIOL_1002")
        self.add_course("BIOL_2010", "BIOL_2020")
        self.add_course("BIOL_2010", "EXSC_3830")
        self.add_course("EXSC_3830", "EXSC_4000")
        self.add_course("EXSC_3830", "EXSC_4230")
        self.add_course("EXSC_3830", "EXSC_4240")
        self.add_course("EXSC_4000", "EXSC_4010")
        self.add_course("EXSC_4240", "EXSC_4260")

    def convertingFromJson(self):
        """Converts JSON course data into a directed graph format and saves it to a .txt file."""
    input_file = input("Enter the name of the JSON file obtained from the Prerequisite Scraper (including .json extension): ").strip()

    try:
        # Read the JSON data from the input file
        with open(input_file, 'r') as f:
            course_data = json.load(f)

        # Prepare the data in the desired directed graph format
        converted_data = []
        for course, details in course_data.items():
            prerequisites = details.get("prerequisites", [])
            if prerequisites:
                for prereq in prerequisites:
                    converted_data.append(f"{prereq} {course}")
            else:
                converted_data.append(f"NONE {course}")

        # Create a new .txt file to store the converted data
        output_file = "converted_courses.txt"
        with open(output_file, 'w') as f:
            f.write("\n".join(converted_data))

        # Inform the user of the successful creation and location of the file
        print(f"Conversion successful! The new file '{output_file}' has been created at:")
        print(os.path.abspath(output_file))

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found. Please try again.")
    except json.JSONDecodeError:
        print(f"Error: The file '{input_file}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    def update_courses(self):
    # Request user input for the JSON file directory
        user_file = input("Enter the directory of the JSON file obtained from Degree Works: ")

        try:
            # Load the user-provided JSON file
            with open(user_file, 'r') as file:
                user_data = json.load(file)
        
            # Load the stored JSON file (assumed to be named storedCourses.json)
            with open('allCoursesFromPreReqScraper.json', 'r') as stored_file:
                stored_data = json.load(stored_file)

            # Remove completed courses from the stored data
            for course, info in user_data.items():
                if info["status"] == "CourseStatus.COMPLETE" and course in stored_data:
                    del stored_data[course]
        
            # Write the updated data to a new JSON file
            new_file = 'newCoursesToComplete.json'
            with open(new_file, 'w') as output_file:
                json.dump(stored_data, output_file, indent=4)
        
            # Indicate the creation of the new file to the user
            print(f"The new file '{new_file}' has been created at: {os.path.abspath(new_file)}")

        except FileNotFoundError as e:
            print(f"Error: {e}. Please make sure the file paths are correct.")
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON. Ensure the file contains valid JSON.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def main():
    scheduler = DiGraph()
    filename = input("Enter the name of the text file containing those courses from the prereq scraper converted to a directed graph. (or press Enter to run test cases): ").strip()

    try:
        if not filename:
            print("No filename provided. Running test cases...")
            scheduler.load_test_cases()
        else:
            scheduler.load_courses_from_file(filename)

        # Remove "NONE" from vertices if present
        scheduler.vertices.discard("NONE")

        order = scheduler.topological_sort()
        print("Course order (topological sort):", order)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    scheduler.update_courses()
    scheduler.convertingFromJson()
    

if __name__ == "__main__":
    main()