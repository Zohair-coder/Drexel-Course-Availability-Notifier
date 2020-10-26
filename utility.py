from email.mime.text import MIMEText
import smtplib
import ssl
from time import sleep
import requests
from bs4 import BeautifulSoup


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
        if len(course) == 2 and course[0].isalpha() and course[1].isalnum():
            isValid = True
        else:
            print("Invalid input.")

    if course[0].islower():
        course[0] = course[0].upper()
    return course


def getConfig():
    """
    get the configuration filled out by the user in the CONFIG.txt file and store the values into a list called
    configuration_list.

    Arguments: None

    Returns: configuration set by user in CONFIG.txt (list) 
    """
    # if CONFIG.txt exists, open it. Otherwise throw an error.
    try:
        configuration_text = open("CONFIG.txt", "r")
    except:
        raise Exception(
            'CONFIG.txt not found. Are you sure you renamed CONFIG_DEV.txt to CONFIG.txt before starting the program?')
    configuration_list = []
    for info in configuration_text.readlines():
        # separate the prompt from the value in CONFIG.txt. Remove the \n at the end.
        configuration_list.append(info.split(": ")[1][:-1])
    configuration_text.close()
    return configuration_list


def sendMessage(subject, message):
    print("Sending email...")
    message = MIMEText(message)
    message['Subject'] = subject
    message['From'] = SENDER_EMAIL
    message['To'] = RECEIVER_EMAIL
    sent = False
    while not sent:
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=CONTEXT) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL,
                                message.as_string())
                sent = True
        except:
            print("Error while sending email. Trying again in 10 seconds")
            sleep(10)
    print("Sent.")


def getSoup(url):
    """
    Function that takes a url as input and returns the soup as output.
    If there's an error in fetching data, it requests it again after CHECK_EVERY seconds.
    """
    getting_data = True
    while getting_data:
        try:
            raw_data = requests.get(url, timeout=10)
            getting_data = False
        except:
            print(
                "Error while requesting data. Trying again in {} seconds".format(CHECK_EVERY))
            sleep(10)
    soup = BeautifulSoup(raw_data.content, "html.parser")
    return soup


def getData(data, soup):
    status = "CLOSED"
    table_data = soup.select("td")
    for td in table_data:
        if td.get_text() == data:
            status = td.findNext('td').get_text()
    return status


PORT = 465  # For SSL
CONTEXT = ssl.create_default_context()  # required for sendMail function
CONFIG = getConfig()
# store the information from CONFIG.txt into global variables
SENDER_EMAIL = CONFIG[0]
SENDER_PASSWORD = CONFIG[1]
RECEIVER_EMAIL = CONFIG[2]
# send an email every NOTIFY_IN amount of hours to let them know the program is running and has not found an open seat yet
NOTIFY_IN = int(CONFIG[3])
# check the Drexel website every CHECK_EVERY amount of seconds
CHECK_EVERY = int(CONFIG[4])
