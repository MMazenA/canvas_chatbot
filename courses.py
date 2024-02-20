from canvasapi import Canvas
import re
from datetime import datetime, timedelta
import pytz


class Courses():
    def __init__(self, canvas:Canvas) -> None:
        self.paginated_courses = {}
        self.active_courses = []
        self.courses = []
        self.canvas = canvas
        self.max_term = -1

    def append_course(self,cleaned_course):
        """
        Appends all courses to courses object and adds active courses. Appends using a course dict.

        Args:

        cleaned_course : [Code,level,ID,term] i.e. [CSC,3110,172906,241]
        """
        course_dict = {"letter_code":cleaned_course[0],"code":cleaned_course[1],"canvas_id":cleaned_course[2],"term":cleaned_course[3]}
        self.courses.append(course_dict)
        current_course_term  = course_dict["term"]
        if(self.max_term < current_course_term):
            self.max_term = current_course_term
            self.active_courses = []
        if(self.max_term == current_course_term):
            self.active_courses.append(course_dict)

    def _get_single_paginated_course(self,course_id):
        for course in self.paginated_courses:
            if course.__dict__.get("id") == course_id:
                return course
        

    def get_assignments(self,course_id):
        """Retrive assignments for a given course_id"""
        paginated_course = self._get_single_paginated_course(course_id)
        assignments = paginated_course.get_assignments()
        assignment_list = []
        for assignment in assignments:
            assignment = self.clean_assignment(assignment)
            assignment_list.append(assignment)
        return assignment_list
    
    def clean_assignment(self,assignment):
        """
        Removes html tags from given assignment and cleans uneeded keys.
        """
        clean = re.compile('<.*?>|&.*?;')
        cleaned_description = re.sub(clean, '', str(assignment.__dict__.get("description")))
        assignment.__dict__["description"] = cleaned_description
        key_removal_list = ["secure_params", "submissions_download_url", "lti_context_id",
                    "intra_group_peer_reviews", "graders_anonymous_to_graders",
                    "grader_names_visible_to_final_grader", "grader_count",
                    "grader_comments_visible_to_graders", "moderated_grading",
                    "max_name_length", "grading_standard_id", "important_dates",
                    "final_grader_id", "anonymous_grading", "automatic_peer_reviews",
                    "anonymous_instructor_annotations", "can_duplicate"]
        for key in key_removal_list:
            assignment.__dict__.pop(key, None)

        return assignment
    
    def get_active_assignments(self,day_filter,time_zone="EST"):
        """
        Given a course_id, provide all those that are due in the future or under a day filter for that given class.

        Args:
        assignments: paginated list of assignments
        filter: days from today that you want to observe 
        """
        time_zone = pytz.timezone(time_zone)
        active_assignments = []
        for course in self.active_courses:
            course_id = course["canvas_id"]
            assignments = self.get_assignments(course_id)
            for assignment in assignments:
                due_date = assignment.__dict__.get("due_at_date")
                assignment.__dict__["course_info"] = course
                undated = due_date == None
                if undated:
                    continue #skip undated assignmnets, not handling those
                due_date= due_date.astimezone(time_zone)
                now_date = datetime.now().astimezone(time_zone)
                filter_date = (datetime.now() + timedelta(days=day_filter)).astimezone(time_zone)
                viewable_date = now_date < due_date and due_date< filter_date
                if(not viewable_date):
                    continue
                active_assignments.append(assignment)
        return active_assignments
    

    def set_paginated_courses(self, paginated_courses):
        self.paginated_courses = paginated_courses

    def print_active_courses(self):
        for course_dict in self.active_courses:
            print(list(course_dict.values()))
    


