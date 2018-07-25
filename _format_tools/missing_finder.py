import re
from bs4 import BeautifulSoup

cv_data = open("../.suspended_pages/conferences_list.txt")
html_data = open("../.suspended_pages/publications.html")

cv_list = []
html_list = []
missing_list = []

for line in cv_data:
    cv_list.append(((re.sub(r"[^\w\n]", "", line)).strip().lower()))

for line in html_data:
    html_list.append(((re.sub(r"[^\w\n]", "", line)).strip().lower()))

for conference in cv_list:
    truth_value = 0
    for i in range(0, len(html_list)):
        if conference in html_list[i]:
            truth_value = 1
    if not truth_value:
        missing_list.append(conference)

[print(title + "\n") for title in missing_list]
