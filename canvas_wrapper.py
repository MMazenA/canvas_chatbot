from canvasapi import Canvas
import os
from courses import Courses


class CanvasWrapper():
    def __init__(self, canvas:Canvas) -> None:
        self.canvas = canvas
        self.account = canvas.get_current_user()
        self.courses = Courses(self.canvas)
        for course in self._retrive_enrolled_courses():
            self.courses.append_course(course)
        # self.courses.get_active_assignments()

    
    def _clean_course_code(self, course_code,course_id):
        """
        Accepts raw course_code i.e.CSC_4500_2309_002 and converts to array [CSC,4500].
        """
        formatted_code = course_code.split("_")[0:2]
        if(len(formatted_code)>=2 and formatted_code[1].isdigit()):
            return course_code.split("_")[0:2] + [course_id] 
        return "Inapplicable"
    
    def _retrive_enrolled_courses(self):
        """
        Retrive enrolled courses for the given user, [Code,level,ID,term] i.e. [CSC,3110,172906,241]
        """
        courses = self.account.get_courses()
        self.courses.set_paginated_courses(courses)
        enrolled_courses = []
        for course in courses:
            student = course.__dict__.get("enrollments",[{"type":"N/A"}])[0]["type"] == "student"
            if not student:
                continue
            course_code = course.__dict__.get("course_code")
            course_id = course.__dict__.get("id")
            course_term = course.__dict__.get("enrollment_term_id")

            if course_code is None:
                continue
            formatted_course_code = self._clean_course_code(course_code,course_id)
            if formatted_course_code == "Inapplicable":
                continue
            formatted_course_code.append(course_term)
            enrolled_courses.append(formatted_course_code)
        return enrolled_courses
    def print_active_courses(self):
        self.courses.print_active_courses()

    def get_active_assignments(self,day_filter=365):
        return self.courses.get_active_assignments(day_filter=day_filter)
        
def main():
    API_URL = "https://canvas.wayne.edu"
    API_KEY = os.environ["CANVAS_TOKEN"]
    canvas = CanvasWrapper(Canvas(API_URL, API_KEY))
    canvas.print_active_courses()
    assignments = canvas.get_active_assignments()

    
if __name__=="__main__":
    main()