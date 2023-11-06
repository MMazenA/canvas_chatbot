from canvasapi import Canvas
import os
import requests
import pprint

API_URL = "https://canvas.wayne.edu"
API_KEY = os.environ["CANVAS_TOKEN"]

# canvas = Canvas(API_URL, API_KEY)
# 162831
data = requests.get(
    "https://canvas.instructure.com/api/" + "/v1/courses?access_token=" + API_KEY
)
print(data.status_code)
# print(len(data.json()))
# pprint.pprint(data.json())
# data = requests.get(API_URL + "/v1/users?access_token=" + API_KEY)
# print(data.status_code)
# pprint.pprint(data.json())


# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
account = canvas.get_current_user()
print(account)
courses = account.get_courses()
print(courses[0].__dict__.keys())
print()
course_num = 33
print(
    courses[course_num].__dict__.get("name"),
    courses[course_num].__dict__.get("id"),
    courses[course_num].get_modules(),
    "\n\n",
)
for module in courses[course_num].get_modules():
    print(module)
print(courses)
    