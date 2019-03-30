import requests
from bs4 import BeautifulSoup
import re

# Downloads the webpage
billboard = requests.get("https://www.billboard.com/charts/")

# Parse the webpage
# webpage = BeautifulSoup(billboard.text, 'html.parser')

# print(webpage.prettify())

# Use this temporarily to prevent downloading the webpage multiple times
file = open('index.html', 'r')
webpage = BeautifulSoup(file.read(), 'html.parser')

# Find the chart list
chart = webpage.find_all(class_='chart-panel__item chart-panel__item--selector')
# chart = webpage.find(class_='chart-panel chart-panel--main')
# chart = webpage.find(class_='chart-panel__item')
# chart = webpage.find_all(class_='chart-panel__text')

# Create a list of categories
categories = []
for tag in chart:
	categories.append(''.join(tag.div.contents).replace(" ", "").replace("\n", ""))

# Show list of categories
for i in range(len(categories)):
	print(i + 1, ") ", categories[i], sep='')

# print(chart)
# for x in chart:
# 	print(x.div.contents)

# a = filter(regex.search, x.div.contents)
# print(a)

# for i in filter(regex.search, x.div.contents):
# 	print(i)

# print(webpage)

# soup = BeautifulSoup()