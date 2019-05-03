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
	# Magic formatting of the list to remove the whitespace and newlines (could be improved)
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

# Get all the charts from the category using the category name and css class
charts = webpage.find(id=categoriesList[categorySelection].replace(' ','').replace('/','').lower() + 'ChartPanel').find_all(class_="chart-panel__text")

# Fix the charts formatting
chartsList = []
for tag in charts:
	chartsList.append(' '.join(''.join(tag.contents).split()))

numberOfCharts = len(charts)

# Show list of categories
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

# Get the link for the chart
chart = charts[chartSelection].parent.parent['href']

# YEAR SELECTION

print("Enter the dates you would like to parse from:")

# Get the starting date
print("Starting Date: ", end="")
while True:
	try:
		# Get the desired start date
		startDate = dateparser.parse(input())
		# Set the date to be the next Saturday, or previous Saturday if the next Saturday hasn't happened yet
		startDate += timedelta(days=((5 - startDate.weekday()) % 7))
		if startDate.date() > datetime.now().date():
			startDate -= timedelta(days=7)
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
		# Set the date to be the next Saturday, or previous Saturday if the next Saturday hasn't happened yet
		endDate += timedelta(days=((5 - endDate.weekday()) % 7))
		if endDate.date() > datetime.now().date():
			endDate -= timedelta(days=7)
		# Make sure the date is between the start date and now
		if startDate.date() <= endDate.date() <= datetime.now().date():
			break
		raise Exception
	except Exception:
		endDate = print("Please enter a valid date: ", end="")

# PARSE THE WEBPAGES

# Stores the songs in a dictionary for counting occurances
songDictionary = {}

# Date stores the current date
date = startDate

# Get the url for what to parse
currentURL = url + chart + "/%d-%02d-%02d" % (date.year, date.month, date.day)

# Run until completion
while True:
	# Print out the current date to ensure it is working
	print("Parsing: ", date.date(), sep="")
	# Download the current dates song list
	week = BeautifulSoup(requests.get(currentURL).text, 'html.parser')
	# The songs are split into five chuncks or 'blocks', each containing 20 songs, parse each of them
	songBlocks = week.select(".chart-list.chart-details__left-rail")
	# Iterate through each block and add its songs to the dictionary
	for block in songBlocks:
		# Get the list of songs for the block
		songList = block.find_all("div", "chart-list-item")
		# Iterate through each song in the block
		for songEntry in songList:
			# Create tuple as dictionary keys
			key = (songEntry['data-artist'], songEntry['data-title'])
			# Reverse the order of the ranking (#1 song is now the length of the list, not necessarily 100)
			rank = len(songBlocks) * len(songList) + 1 - int(songEntry['data-rank'])
			# Check if the song is in the dictionary already, if it is, then add its rank, else add it to the dictionary
			if key in songDictionary.keys():
				songDictionary[key] += rank
			else :
				songDictionary[key] = rank
	# Exit condition			
	if date >= endDate:
		break		
	# Set the new current url for the next iteration			
	currentURL = url + week.select('.dropdown__date-selector-option')[1].a['href']
	# Get the next date from the url (last 10 characters)
	date = dateparser.parse(currentURL[-10:])

# Convert the dictionary into a list that is sorted based on the key values (rank)
rankedSongs = sorted(songDictionary, key=songDictionary.get)
# Reverse the list so the highest rank is in front of the list
rankedSongs.reverse()
# Display the list
for rank in range(min(len(rankedSongs), 100)):
	print(rank + 1, ") ", rankedSongs[rank][1], " - ", rankedSongs[rank][0], sep='')