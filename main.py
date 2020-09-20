#!/usr/bin/env python3

import drexel_course_availability
import drexel_course_url_finder

url, course = drexel_course_url_finder.find()
drexel_course_availability.Notifier(url, course)
