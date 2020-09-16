from time import sleep
import requests
from bs4 import BeautifulSoup
from notify_run import Notify
notify = Notify()


def courseAvailabilityNotifier(url, course="your course", timeout=10):
    while True:
        raw_data = requests.get(url)

        soup = BeautifulSoup(raw_data.content, "html.parser")

        table_data = soup.select("td")
        for td in table_data:
            if td.get_text() == "Enroll":
                status = td.findNext('td').get_text()

        print("Status {}: {}".format(course, status))
        if status == "CLOSED":
            # notification = "Seats for " + course +" not available"
            # notify.send("Seats for CI 102 not available")
            print()
        else:
            notification = "Status: " + status
            notify.send(notification)

        sleep(timeout)
