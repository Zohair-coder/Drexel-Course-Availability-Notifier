#!/usr/bin/env python3

import course_notifier
import course_url_finder

url = course_url_finder.find()
course_notifier.Notifier(url)
