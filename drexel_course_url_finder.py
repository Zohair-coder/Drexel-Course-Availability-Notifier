from time import sleep
import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://termmasterschedule.drexel.edu"
PAYLOAD = {'component': 'collSubj',
           'page': 'CollegesSubjects', 'service': 'direct'}
COMPONENT = "component=collSubj"
PAGE = "page=CollegesSubjects"
SERVICE = "service=direct"
SP2 = ""


def find():
    sp1 = printAndFindSeasonSP1()
    printColleges()
    chosen_college = input("Please select your college index: ")
    find_course = input("Please enter the course code (EXMPL 101): ")
    # creates list with first element containing code string and second element containing code number
    print("Finding your course name...")
    find_course = find_course.split()
    courses_data = findCourse(chosen_college, find_course, sp1)
    print("Done.")
    print("Finding all sections of your course...")
    shortlisted_urls = findSections(courses_data, find_course)
    print("Done.")

    final_course_index = int(input("Please select the course index: "))
    final_course_url = shortlisted_urls[final_course_index][0]

    return(BASE_URL + final_course_url["href"])


def printColleges():
    colleges = {"Antoinette Westphal COMAD": 0,
                "Arts and Sciences": 1, "Bennett S. LeBow Coll. of Bus.": 2, "Center for Civic Engagement": 3, "Close Sch of Entrepreneurship": 4, "Col of Computing & Informatics": 5, "College of Engineering": 6, "Dornsife Sch of Public Health": 7, "Goodwin Coll of Prof Studies": 8, "Graduate College": 9, "Miscellaneous": 10, "Nursing & Health Professions": 11, "Pennoni Honors College": 12, "Sch.of Biomed Engr,Sci & Hlth": 13, "School of Education": 14}
    for college, index in colleges.items():
        print(index, "    ", college)


def findCourse(chosen_college, find_course, sp1):

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
            if find_course[0] == code:
                courses_data = requests.get(
                    BASE_URL + link['href'])
    return courses_data


def findSections(courses_data, find_course):
    courses_soup = BeautifulSoup(courses_data.content, "html.parser")
    table_rows = courses_soup.select("tr")

    shortlisted_course_data = []
    shortlisted_course_urls = []
    for row in table_rows:
        for data in row:
            if find_course[1] in data:
                if row.get_text():
                    shortlisted_course_data.append(row.get_text())
                    shortlisted_course_urls.append(row.select("a"))

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
            print(len(seasons_links), link.get_text())

    print()
    season_choice_index = int(input("Select the index: "))
    final_link = seasons_links[season_choice_index - 1]['href']

    variables = final_link.split('&')

    for variable in variables:
        if 'sp' in variable:
            sp1 = variable
    return sp1


if __name__ == "__main__":
    print("URL:", find())
