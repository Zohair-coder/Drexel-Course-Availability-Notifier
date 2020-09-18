#!/usr/bin/env python3

from course_availability_v8 import courseAvailabilityNotifier
from course_url_finder_v2 import find_course_url

url = find_course_url()
courseAvailabilityNotifier(url)
