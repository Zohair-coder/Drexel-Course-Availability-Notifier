"""
Program that gives you information about a course. Not required for Drexel Course Availability Notifier.
Added just for convenience.
To start, execute: 
"python drexel_course_information.py"
in your terminal.
"""


import course_url_finder
import utility
from tabulate import tabulate


def getTimeAndDays(soup):
    table_data = soup.select("td")
    for td in table_data:
        if td.get_text()[-2:] == "pm" or td.get_text()[-2:] == "am":
            return td.get_text() + " - " + td.findNext('td').get_text()
    return None
    # fake comment


url = course_url_finder.find()
soup = utility.getSoup(url)


class_details = [["CRN ", utility.getData("CRN", soup)], [
    "Section ", utility.getData("Section", soup)],
    ["Credits ", utility.getData("Credits", soup)],
    ["Title ", utility.getData("Title", soup)],
    ["Campus ", utility.getData("Campus", soup)],
    ["Instructor ", utility.getData(
        "Instructor(s)", soup)],
    ["Instruction Type ", utility.getData(
        "Instruction Type", soup)],
    ["Instruction Method ", utility.getData(
        "Instruction Method", soup)],
    ["Max Enroll ", utility.getData("Max Enroll", soup)],
    ["Enroll ", utility.getData("Enroll", soup)],
    ["Time and Days ", getTimeAndDays(soup)],
]

print(tabulate(class_details))
