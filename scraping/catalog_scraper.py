import json
import requests
from bs4 import BeautifulSoup, Tag

class CourseManager:
    def __init__(self, catalog_url: str):
        self.catalog_url = catalog_url
        # self.prereqs = self.get_course_prereqs()

    def get_course_list(self, stripped=False):
        """
        Returns a list of courses from the catalog 
        in the form of a list of beautiful soup objects
        """
        try:
            page = requests.get(catalog)
            soup = BeautifulSoup(page.content, 'html.parser')
            course_list = soup.find_all("h2", class_="course-name")
            if stripped:
                course_list = [course.text.strip() for course in course_list]
            return course_list
        except:
            print("Error: Could not get course list")

    def get_course_code(self, course_name: str | Tag):
        """
        Takes in a course name in the form of a string or bs4 Tag.
        Returns a course code from the catalog 
        in the form of a string
        """
        try:
            if isinstance(course_name, Tag):
                course_name = course_name.find("span")
                return course_name.text.strip()
            
            course_code = " ".join(course_name.split(" ")[:2])
            return course_code
        except:
            print("Error: Could not get course code")

    def get_course_prereqs(self):
        """
        Takes in a list of bs4 Tag objects.p
        Returns a course prerequisites from the catalog 
        in the form of a dictionary of a course name and 
        its prereqs
        """
        try:
            course_list = self.get_course_list()
            prereqs = {}
            for course in course_list:
                # extra_fields is a DOM element that contains course preqrequesites
                extra_fields = course.find_next("div", class_="extraFields")
                # If the course has no prereqs, then the extra_fields element will be None
                if not extra_fields or \
                    extra_fields.find_previous_sibling(
                        "h2", class_="course-name").text.strip() != course.text.strip() or \
                            extra_fields.find("h4").text.strip() != "Requirements":
                    
                    course_prereqs = {}
                else:
                    course_prereqs = extra_fields.find("p").text.strip()
                    course_prereqs = course_prereqs[course_prereqs.find(' ')+1:].replace(".", "")
                    course_prereqs = self._process_prerequisites(course_prereqs)

                course_name = self.get_course_code(course.text.strip())
                prereqs[course_name] = course_prereqs
            return prereqs
        except Exception as e:
            print(f"Error: Could not get course prereqs. {e})")

    def save_to_json(self, path, data):
        """
        Takes in a path to a json file and a dictionary of data.
        Saves the data to the json file
        """
        try:
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
        except:
            print("Error: Could not save to json file")

    def _process_prerequisites(self, prerequisites):
        """
        Takes in a string of course prereqs.
        Returns a dictionary of course prereqs
        """
        if prerequisites == "None":
            return "None"

        def cleanup(conditions):
            return list(filter(None, map(lambda condition: condition.strip(), conditions)))


        def parse_conditions(condition_str):
            conditions = cleanup(condition_str.split(" or "))
            if len(conditions) > 1:
                return {"OR": conditions}
            else:
                return conditions[0]

        def parse_and_condition(and_condition_str):
            and_conditions = cleanup(and_condition_str.split(" and "))
            if len(and_conditions) > 1:
                return {"AND": [parse_conditions(cond) for cond in and_conditions]}
            else:
                return parse_conditions(and_conditions[0])

        prerequisites_dict = {}
        course_list = prerequisites.split(";")
        if len(course_list) > 1:
            prerequisites_dict["AND"] = [parse_and_condition(cond) for cond in course_list]
        else:
            prerequisites_dict = parse_and_condition(course_list[0])

        return prerequisites_dict

if __name__ == "__main__":
    catalog = "https://ucsc.smartcatalogiq.com/en/current/general-catalog/courses/cse-computer-science-and-engineering/"
    cse = CourseManager(catalog)
    course = cse.get_course_prereqs()
    cse.save_to_json("cse.json", course)