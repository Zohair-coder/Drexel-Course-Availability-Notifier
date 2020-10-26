from time import sleep
import requests
from bs4 import BeautifulSoup
import re
import sys
from tabulate import tabulate
import utility

BASE_URL = "https://termmasterschedule.drexel.edu"
PAYLOAD = {'component': 'collSubj',
           'page': 'CollegesSubjects', 'service': 'direct'}
COMPONENT = "component=collSubj"
PAGE = "page=CollegesSubjects"
SERVICE = "service=direct"


def find():
    """
    Main function of this module that finds the URL of a course input by the user.

    Arguments: None

    Returns: URL of the course page (string)
    """
    sp1 = printAndFindSeasonSP1()
    # creates list with first element containing code string and second element containing code number
    target_course = utility.inputCourse()
    print(
        "Finding all {} courses... \n".format(target_course[0]))
    courses_data = findCourse(target_course, sp1)
    print("Finding all sections of {} {}...".format(
        target_course[0], target_course[1]))
    shortlisted_urls = findSections(courses_data, target_course)
    print("Done.")

    final_course_index = utility.inputIndex(max=len(shortlisted_urls) - 1)
    final_course_url = shortlisted_urls[final_course_index][0]

    return(BASE_URL + final_course_url["href"])


def findCourse(target_course, sp1):
    """
    Goes to every college's page (determined by sp2, which is an integer from 0-14. Every number from 0-14 has a
    unique college assigned to it. For example, sp2=5 means CCI) for the selected season (determined by sp1) and searches
    for the first part of the course code (e.g. for EXMPL 101, it searches for EXMPL). Once this is found, it goes to
    the page that contains all sections for the first part of the course code so that the second part of the course
    code can be found at that page. Returns the data received by going to the page.

    Arguments:
    1. The course that the user wants to find e.g. EXMPL 101 (list of strings)
    2. The part of the url that determines the quarter season aka sp1 (string)

    Returns: The data of the page that contains all the sections of the first part of the target_course (requests object).
    """
    courses_data = None
    for checking_college in range(15):
        colleges = ["Antoinette Westphal COMAD",
                    "Arts and Sciences", "Bennett S. LeBow Coll. of Bus.", "Center for Civic Engagement", "Close Sch of Entrepreneurship", "Col of Computing & Informatics", "College of Engineering", "Dornsife Sch of Public Health", "Goodwin Coll of Prof Studies", "Graduate College", "Miscellaneous", "Nursing & Health Professions", "Pennoni Honors College", "Sch.of Biomed Engr,Sci & Hlth", "School of Education"]
        print("Checking for {} in {}...".format(
            target_course[0], colleges[checking_college]))
        sp2 = "sp={}".format(checking_college)
        college_url = "{BASE_URL}/webtms_du/app?{COMPONENT}&{PAGE}&{SERVICE}&{sp1}&{sp2}".format(
            BASE_URL=BASE_URL, COMPONENT=COMPONENT, PAGE=PAGE, SERVICE=SERVICE, sp1=sp1, sp2=sp2)

        college_soup = utility.getSoup(college_url)

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
                    print("{} found in {}!\n".format(
                        target_course[0], colleges[checking_college]))
                    return courses_data
        print("Not found\n")
    # if the entire loop runs and value of courses_data remains None, the following line will run. Otherwise it will not.
    sys.exit("Course {} not found.")


def findSections(courses_data, target_course):
    """
    Checks the page for all elements that match the second part of the target_course e.g. the 101 part in EXMPL 101.
    Multiple elements might have this second part, since there are many classes for one course.
    Prints all the data of the elements that match the second part.
    Returns the URLs of the pages of all classes that match the target_course.
    Does not ask the user to input the class they want despite printing all the classes.

    Arguments:
    1. The data for the page that has information about the first part of target_course e.g. the EXMPL part in EXMPL 101.
        This page has the data for all sections of EXMPL (requests object).
    2. The target_course that the user wants to get notifications for (list of strings).
    """
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
        sys.exit("No sections found for your course {} {} were found.".format(
            target_course[0], target_course[1]))

    # a list that holds the same data as shortlisted_course_data but in a better formatted way
    aesthetic_course_data = []
    for info in shortlisted_course_data:
        info = info.split("\n")

        # remove empty elements
        while '' in info:
            info.remove('')

        # add a newline character at the end of every data element so that when it is tabulated,
        #  there is an empty row between two rows, making the table easier to read
        for index, element in enumerate(info):
            info[index] = element + "\n "
        aesthetic_course_data.append(info)

    print(tabulate(aesthetic_course_data, showindex=True))
    print()
    print()
    return shortlisted_course_urls


def printAndFindSeasonSP1():
    """
    Searches for all links from Drexel Term Master and displays the ones that have the text "Quarter" inside their HTML tag.
    Prompts the user to select one of the printed Quarters.
    Grabs the link of the selected quarter and stores the "sp" part of the URL, since this is the only part of the URL
    that is required to identify the quarter.

    Arguments: None

    Returns: The "sp" part of the URL that is required to identify the quarter season (string).
    """
    soup = utility.getSoup(BASE_URL)

    links = soup.select("a")

    seasons_links = []
    seasons = []
    for link in links:
        if "Quarter" in link.get_text():
            seasons_links.append(link)
            # print(len(seasons_links) - 1, link.get_text())
            seasons.append([link.get_text()])
    print()
    print(tabulate(seasons, headers=["Index", "Seasons"], showindex=True))
    season_choice_index = utility.inputIndex(max=len(seasons_links) - 1)
    final_link = seasons_links[season_choice_index]['href']

    variables = final_link.split('&')

    for variable in variables:
        if 'sp' in variable:
            sp1 = variable
    return sp1


if __name__ == "__main__":
    print("URL:", find())
