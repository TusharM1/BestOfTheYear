import requests
from bs4 import BeautifulSoup
import dateparser
from datetime import datetime, timedelta, date

# INTODUCTION TEXT

print("Billboard Chart Parser")
print("This tool will parse the billboard.com website to find the best songs")
print("Working as of March 30th, 2019\n")




# DOWNLOAD WEBPAGE

url = "https://www.billboard.com"

# Downloads the webpage
# billboard = requests.get(url + "/charts/")

# Parse the webpage
# webpage = BeautifulSoup(billboard.text, 'html.parser')

# Use this temporarily to prevent downloading the webpage multiple times
file = open('index.html', 'r')
webpage = BeautifulSoup(file.read(), 'html.parser')




# CATEGORY SELECTION

# Find the categories list
categories = webpage.select('.chart-panel__item.chart-panel__item--selector')

# Create a list of categories
categoriesList = []
for tag in categories:
	categoriesList.append(' '.join(''.join(tag.div.contents).split()))

numberOfCategories = len(categoriesList)

# Show list of categories
print("List of Categories:")
for i in range(numberOfCategories):
	print(i + 1, ") ", categoriesList[i], sep='')
print()

# Select a category
categorySelection = input("Select a category below by its listed number: ")
while True:
	if categorySelection.isdigit() and 1 <= int(categorySelection) <= numberOfCategories:
		categorySelection = int(categorySelection) - 1
		break
	categorySelection = input("Please enter a valid selection (numbers 1 - " + str(numberOfCategories) + "): ")




# CHART SELECTION

charts = webpage.find(id=categoriesList[categorySelection].replace(' ','').replace('/','').lower() + 'ChartPanel').find_all(class_="chart-panel__text")

chartsList = []
for tag in charts:
	chartsList.append(' '.join(''.join(tag.contents).split()))

numberOfCharts = len(charts)

# Show list of categories and take in a selection input
print("List of Charts:")
for i in range(numberOfCharts):
	print(i + 1, ") ", chartsList[i], sep='')
print()

# Select a chart
chartSelection = input("Select a chart below by its listed number: ")
while True:
	if chartSelection.isdigit() and 1 <= int(chartSelection) <= numberOfCharts:
		chartSelection = int(chartSelection) - 1
		break
	chartSelection = input("Please enter a valid selection (numbers 1 - " + str(numberOfCharts) + "): ")

chart = charts[0].parent.parent['href']

# YEAR SELECTION

print("Enter the dates you would like to parse from:")

# Get the starting date
print("Starting Date: ", end="")
while True:
	try:
		startDate = dateparser.parse(input())
		# Set the date to be the next Saturday
		startDate += timedelta(days=((5 - startDate.weekday()) % 7))
		# Make sure the date is within the allowed time frames (1958 is the oldest available chart date on the website, I think)
		if date(1958, 7, 28) <= startDate.date() <= datetime.now().date():
			break
		raise Exception
	except Exception:
		startDate = print("Please enter a valid date: ", end="")

# Get the starting date
print("Ending Date: ", end="")
while True:
	try:
		endDate = dateparser.parse(input())
		# Set the date to be the next Saturday
		endDate += timedelta(days=((5 - endDate.weekday()) % 7))
		# Make sure the date is between the start date and now
		if startDate.date() <= endDate.date() <= datetime.now().date():
			break
		raise Exception
	except Exception:
		endDate = print("Please enter a valid date: ", end="")

print(startDate, endDate)




# PARSE THE WEBPAGES

songDictionary = {}

date = startDate
currentURL = url + chart + "/%d-%02d-%02d" % (date.year, date.month, date.day)
while date < endDate:
	print("Parsing: ", date.date(), sep="")
	week = BeautifulSoup(requests.get(currentURL).text, 'html.parser')
	songBlocks = week.select(".chart-list.chart-details__left-rail")
	songs = []
	for block in songBlocks:
		songList = block.find_all("div", "chart-list-item")
		for songEntry in songList:
			key = (songEntry['data-artist'], songEntry['data-title'])
			rank = 101 - int(songEntry['data-rank'])
			if key in songDictionary.keys():
				songDictionary[key] += rank
			else :
				songDictionary[key] = rank
			songs.append([songEntry['data-rank'], songEntry['data-artist'], songEntry['data-title']])
	currentURL = url + week.select('.dropdown__date-selector-option')[1].a['href']
	date = dateparser.parse(currentURL[-10:])

rankedSongs = sorted(songDictionary, key=songDictionary.get)
rankedSongs.reverse()

for rank in range(100):
	print(rank + 1, ") ", rankedSongs[rank][1], " - ", rankedSongs[rank][0], sep='')

