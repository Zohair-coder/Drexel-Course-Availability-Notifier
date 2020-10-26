from time import sleep
import requests
from bs4 import BeautifulSoup
import datetime
from sys import argv
from sys import exit
import utility


def Notifier(url):
    # start counting the time
    begin_time = datetime.datetime.now()

    soup = utility.getSoup(url)
    # send an email to let the user know that everything is working in order
    message = "You have started the Drexel Course Availability program. You will receive updates on {} {} every {} hours.".format(
        getData("Subject Code", soup), getData("Course Number", soup), utility.NOTIFY_IN)
    utility.sendMessage("Course Availability Email",
                        message)
    print("Checking for available seats every {} seconds...".format(
        utility.CHECK_EVERY))
    while True:
        soup = utility.getSoup(url)

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
            utility.sendMessage(subject, message)
            break
        reset_time = updateNotification(begin_time, message, course)
        if reset_time:
            begin_time = datetime.datetime.now()

        sleep(utility.CHECK_EVERY)


def updateNotification(begin_time, message, course):
    if not utility.NOTIFY_IN:
        return False
    elapsed = datetime.datetime.now() - begin_time
    seconds = elapsed.days*86400 + elapsed.seconds  # drop microseconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    if hours >= utility.NOTIFY_IN:
        message = "{} Hour Update: {}".format(utility.NOTIFY_IN, message)
        subject = "{} Availability Update".format(course)
        utility.sendMessage(subject, message)
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
    url = input("URL: ")
    Notifier(url)


if __name__ == "__main__":
    main()
# url = "https://termmasterschedule.drexel.edu/webtms_du/app?component=courseDetails&page=CourseList&service=direct&sp=ZH4sIAAAAAAAAADWLOw7CMBAFlyA%2BNaInF8B2LFFRgqjSIHKBJV5FQXZI7A2k4kRcjTtgFPHKeTPvD8yChw2ZXhhPA1lRexZPurILwiCjKMg7GDdJYJrDAksuakcM6%2FyGD5Shs%2FIHAqNr9zksOSaHu4nGajQsNpW8sK%2Bb6v8fKZQdvCAZ2pZhrpVW2S4GJ7Q2Pffoo5RqtdXZFwRRPMmkAAAA&sp=SCI&sp=SCS&sp=S15834&sp=S164&sp=5"
# courseAvailabilityNotifier(url)
