from canvasapi import Canvas
import os
import requests
import pprint

API_URL = "https://canvas.wayne.edu"
API_KEY = os.environ["CANVAS_TOKEN"]
canvas = Canvas(API_URL, API_KEY)

def main():
    account = canvas.get_current_user()
    print(account)
    courses = account.get_courses()
    print(courses[0].__dict__.keys())
    print()

    enrolled_courses = []
    for course in courses:
        course_code = course.__dict__.get("course_code")
        course_id = course.__dict__.get("id")
        print(course_code, course.__dict__.get("enrollment_term_id"))
        if course_code is None:
            continue
        formatted_course_code = clean_course_code(course_code,course_id)
        if formatted_course_code == "Inapplicable":
            continue
        enrolled_courses.append([formatted_course_code])
    # print(enrolled_courses)
    print()
    print(get_assignments(196510))

def clean_course_code(course_code,course_id):
    """
    Accepts raw course_code i.e.CSC_4500_2309_002 and converts to array [CSC,4500].
    """
    formatted_code = course_code.split("_")[0:2]
    if(formatted_code[1].isdigit()):
        return course_code.split("_")[0:2] + [course_id] 
    return "Inapplicable"

def get_assignments(course_id):
    course = canvas.get_course(course_id)
    print(course.__dict__.get("course_code"))
    assignments = course.get_assignments()
    assignment_list = []
    for assignment in assignments:
        assignment_list.append(assignment)
    return assignment_list
    

if __name__=="__main__":
    main()