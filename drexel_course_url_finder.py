from time import sleep
import requests
from bs4 import BeautifulSoup
import re
import sys

BASE_URL = "https://termmasterschedule.drexel.edu"
PAYLOAD = {'component': 'collSubj',
           'page': 'CollegesSubjects', 'service': 'direct'}
COMPONENT = "component=collSubj"
PAGE = "page=CollegesSubjects"
SERVICE = "service=direct"
SP2 = ""


def find():
    """
    Main function of this module that finds the URL of a course input by the user.

    Arguments: None

    Returns: URL (string)
    """
    sp1 = printAndFindSeasonSP1()
    chosen_college = printAndInputColleges()
    # creates list with first element containing code string and second element containing code number
    target_course = inputCourse()
    print("Finding your course name...")
    courses_data = findCourse(chosen_college, target_course, sp1)
    print("Done.")
    print("Finding all sections of your course...")
    shortlisted_urls = findSections(courses_data, target_course)
    print("Done.")

    final_course_index = inputIndex(max=len(shortlisted_urls) - 1)
    final_course_url = shortlisted_urls[final_course_index][0]

    return(BASE_URL + final_course_url["href"])


def printAndInputColleges():
    """
    Prints all colleges and asks the user to input the index of the chosen college.

    Arguments: None

    Returns: index of the college chosen by the user (integer)
    """
    colleges = {"Antoinette Westphal COMAD": 0,
                "Arts and Sciences": 1, "Bennett S. LeBow Coll. of Bus.": 2, "Center for Civic Engagement": 3, "Close Sch of Entrepreneurship": 4, "Col of Computing & Informatics": 5, "College of Engineering": 6, "Dornsife Sch of Public Health": 7, "Goodwin Coll of Prof Studies": 8, "Graduate College": 9, "Miscellaneous": 10, "Nursing & Health Professions": 11, "Pennoni Honors College": 12, "Sch.of Biomed Engr,Sci & Hlth": 13, "School of Education": 14}
    for college, index in colleges.items():
        print(index, "    ", college)
    chosen_college = inputIndex(max=len(colleges) - 1)
    return chosen_college


def findCourse(chosen_college, target_course, sp1):
    courses_data = None
    sp2 = "sp={}".format(chosen_college)
    college_url = "{BASE_URL}/webtms_du/app?{COMPONENT}&{PAGE}&{SERVICE}&{sp1}&{sp2}".format(
        BASE_URL=BASE_URL, COMPONENT=COMPONENT, PAGE=PAGE, SERVICE=SERVICE, sp1=sp1, sp2=sp2)
    college_data = requests.get(college_url)

    college_soup = BeautifulSoup(college_data.content, "html.parser")

    links = college_soup.select("a")
    pattern = "\\((.*?)\\)"
    for link in links:
        course_name = link.get_text()
        code = re.search(pattern, course_name)
        if code:
            code = code.group(1)
            if target_course[0] == code:
                courses_data = requests.get(
                    BASE_URL + link['href'])
                break
    if not courses_data:
        sys.exit("Course {} not found.".format(target_course[0]))
    return courses_data


def findSections(courses_data, target_course):
    courses_soup = BeautifulSoup(courses_data.content, "html.parser")
    table_rows = courses_soup.select("tr")

    shortlisted_course_data = []
    shortlisted_course_urls = []
    for row in table_rows:
        for data in row:
            if target_course[1] in data:
                if row.get_text():
                    shortlisted_course_data.append(row.get_text())
                    shortlisted_course_urls.append(row.select("a"))
    if len(shortlisted_course_urls) == 0:
        sys.exit("No sections found for your course {}{} were found.".format(
            target_course[0], target_course[1]))

    aesthetic_course_data = []
    for info in shortlisted_course_data:
        info = info.split("\n")
        while '' in info:
            info.remove('')
        aesthetic_course_data.append(info)

    for index, aesthetic_course_data in enumerate(aesthetic_course_data):
        print(index, end="  ")
        for data in aesthetic_course_data:
            print(data, end="  ")
        print()
    return shortlisted_course_urls


def printAndFindSeasonSP1():
    raw_data = requests.get(BASE_URL)
    soup = BeautifulSoup(raw_data.content, "html.parser")

    links = soup.select("a")

    seasons_links = []
    for link in links:
        if "Quarter" in link.get_text():
            seasons_links.append(link)
            print(len(seasons_links) - 1, link.get_text())

    print()
    season_choice_index = inputIndex(max=len(seasons_links) - 1)
    final_link = seasons_links[season_choice_index]['href']

    variables = final_link.split('&')

    for variable in variables:
        if 'sp' in variable:
            sp1 = variable
    return sp1


def inputCourse():
    """
    Function that prommpts the user to input the course code in the format: "EXMPL 101".
    If the input is not valid(two words, first word composed of alphabet and second word composed of numbers), the user is asked to enter the code again.
    If the first word is in lower-case, it is converted to uppercase.

    Arguments: None

    Returns: List of two elements, with the first element being EXMPL and second element being 101.
    """

    isValid = False
    while not isValid:
        course = input("Please enter the course code (EXMPL 101): ")
        course = course.split()
        if len(course) == 2 and course[0].isalpha() and course[1].isnumeric():
            isValid = True
        else:
            print("Invalid input.")

    if course[0].islower():
        course[0] = course[0].upper()
    return course


def inputIndex(max=float('inf')):
    """
    Function that prompts the user to input the index from the list printed.
    If the input is not a number, the user is prompted to enter it again.

    Arguments: maximum index allowed (integer)

    Returns: index (integer)
    """
    isValid = False

    while not isValid:
        index = input("Please select the index: ")
        if index.isnumeric():
            if int(index) >= 0 and int(index) <= max:
                isValid = True
            else:
                print("Invalid input.")
        else:
            print("Invalid input.")
    return int(index)


if __name__ == "__main__":
    print("URL:", find())
