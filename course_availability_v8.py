from time import sleep
import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
from email.mime.text import MIMEText
import datetime
from sys import argv
from sys import exit

PORT = 465  # For SSL
CONTEXT = ssl.create_default_context()


def getConfig():
    configuration_text = open("CONFIG.txt", "r")
    configuration_list = []
    for info in configuration_text.readlines():
        configuration_list.append(info.split(": ")[1][:-1])
    configuration_text.close()
    return configuration_list


CONFIG = getConfig()

SENDER_EMAIL = CONFIG[0]
PASSWORD = CONFIG[1]
RECEIVER_EMAIL = CONFIG[2]
UPDATE_IN = int(CONFIG[3])
TIMEOUT = int(CONFIG[4])


def courseAvailabilityNotifier(url):
    begin_time = datetime.datetime.now()
    message = "You have started the Drexel Course Availability program on {}. You will receive updates on your course every {} hours.".format(
        begin_time, UPDATE_IN)
    sendMessage("Course Availability Email",
                message)
    print("Checking for available seats every {} seconds...".format(TIMEOUT))
    while True:
        try:
            raw_data = requests.get(url, timeout=10)
        except:
            print(
                "Error while requesting data. Trying again in {} seconds".format(TIMEOUT))
            sleep(10)
            continue
        soup = BeautifulSoup(raw_data.content, "html.parser")
        course = getData("Subject Code", soup) + " " + \
            getData("Course Number", soup)
        status = getData("Enroll", soup)

        message = "\nStatus of " + course + ": " + status
        if status == "CLOSED":
            print("Status {}: {}".format(course, status))
            print()
        else:
            message += " of {} seats filled".format(
                getData("Max Enroll", soup))
            subject = "Seats for {} Available".format(course)
            print(message)
            sendMessage(subject, message)
            break
        reset_time = updateNotification(begin_time, message, course)
        if reset_time:
            begin_time = datetime.datetime.now()

        sleep(TIMEOUT)


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
                server.login(SENDER_EMAIL, PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL,
                                message.as_string())
                sent = True
        except:
            print("Error while sending email. Trying again in 10 seconds")
            sleep(10)
    print("Sent.")


def updateNotification(begin_time, message, course):
    elapsed = datetime.datetime.now() - begin_time
    seconds = elapsed.days*86400 + elapsed.seconds  # drop microseconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    if hours >= UPDATE_IN:
        message = "{} Hour Update: {}".format(UPDATE_IN, message)
        subject = "{} Availability Update".format(course)
        sendMessage(subject, message)
        print("Update sent")
        return True
    return False


def getData(data, soup):
    status = "CLOSED"
    table_data = soup.select("td")
    for td in table_data:
        if td.get_text() == data:
            status = td.findNext('td').get_text()
    return status


def main():
    from course_url_finder_v2 import find_course_url
    url = find_course_url()
    courseAvailabilityNotifier(url)


if __name__ == "__main__":
    main()
# url = "https://termmasterschedule.drexel.edu/webtms_du/app?component=courseDetails&page=CourseList&service=direct&sp=ZH4sIAAAAAAAAADWLOw7CMBAFlyA%2BNaInF8B2LFFRgqjSIHKBJV5FQXZI7A2k4kRcjTtgFPHKeTPvD8yChw2ZXhhPA1lRexZPurILwiCjKMg7GDdJYJrDAksuakcM6%2FyGD5Shs%2FIHAqNr9zksOSaHu4nGajQsNpW8sK%2Bb6v8fKZQdvCAZ2pZhrpVW2S4GJ7Q2Pffoo5RqtdXZFwRRPMmkAAAA&sp=SCI&sp=SCS&sp=S15834&sp=S164&sp=5"
# courseAvailabilityNotifier(url)
