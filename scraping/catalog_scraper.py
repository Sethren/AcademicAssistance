import json
import requests
import re
from bs4 import BeautifulSoup, Tag

class CourseManager:
    def __init__(self, catalog_url: str):
        self.catalog_url = catalog_url
        # self.prereqs = self.get_course_data()

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

    def get_course_data(self):
        """
        Takes in a list of bs4 Tag objects.p
        Returns a course prerequisites from the catalog 
        in the form of a dictionary of a course name and 
        its prereqs
        """
        try:
            course_list = self.get_course_list()
            course_data = {}
            for course in course_list:
                # extra_fields is a DOM element that contains course preqrequesites
                description = course.find_next("div", class_="desc")
                extra_fields = course.find_next("div", class_="extraFields")
                credits = course.find_next("div", class_="credits")
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
                if self._is_graddiv(course_name):
                    break

                course_data[course_name] = course_prereqs
                course_data[course_name] = {
                    'name': course.text.strip().split(" ", 2)[2],
                    'credits': int(credits.text.strip()),
                    'label': course_name.split(" ")[0],
                    'id': course_name.split(" ")[1],
                    # 'description': description.text.strip(),
                    'prerequisites': course_prereqs
                }
            return course_data
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

    def _is_graddiv(self, course_code):
        try:
            course_number = re.search(r'\d+', course_code).group()
            return int(course_number) > 199
        except:
            print("Error: Could not determine if course is upperdiv", course_code)

    def _process_prerequisites(self, prerequisites):
        """
        Takes in a string of course prereqs.
        Returns a dictionary of course prereqs
        """
        if prerequisites == "None":
            return "None"

        def cleanup(conditions):
            cleaned_conditions = []
            for condition in conditions:
                or_conditions = condition.split('or')
                cleaned_or_conditions = [part.strip().replace(',', '').replace(' and ', '') for part in or_conditions]
                cleaned_conditions.extend(cleaned_or_conditions)
            return list(filter(None, cleaned_conditions))

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

        def process_keywords(text):
            keywords = ['concurrent', 'entry', 'level', 'writing', 'mathematics', 'placement']
            if any(keyword in text.lower() for keyword in keywords):
                if 'concurrent' in text.lower():
                    course_code = re.search(r'[A-Z]+\s?\d+[A-Z]*', text).group()
                    return course_code, True
                elif any(keyword in text.lower() for keyword in ['entry', 'level', 'writing']):
                    return 'WRIT 1', True
                elif any(keyword in text.lower() for keyword in ['mathematics', 'math', 'placement']):
                    score = re.search(r'\d+', text)
                    if score:
                        return {"MPE": int(score.group())}, True
            return text, False

        prerequisites_dict = {}
        course_list = prerequisites.split(";")
        if len(course_list) > 1:
            and_conditions = []
            for cond in course_list:
                processed_condition, is_prerequisite = process_keywords(cond)
                if is_prerequisite:
                    and_conditions.append(processed_condition)
            if and_conditions:
                and_conditions.extend([parse_and_condition(cond) for cond in course_list if cond not in and_conditions])
                prerequisites_dict["AND"] = and_conditions
            else:
                prerequisites_dict["AND"] = [parse_and_condition(cond) for cond in course_list]
        else:
            prerequisites_dict = parse_and_condition(course_list[0])

        return prerequisites_dict

if __name__ == "__main__":
    catalog = "https://ucsc.smartcatalogiq.com/en/current/general-catalog/courses/math-mathematics/"
    cse = CourseManager(catalog)
    course = cse.get_course_data()
    cse.save_to_json("math.json", course)