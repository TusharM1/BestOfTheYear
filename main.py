import requests
from bs4 import BeautifulSoup
import datetime

# INTODUCTION TEXT

print("Billboard Chart Parser")
print("This tool will parse the billboard.com website to find the best songs")
print("Working as of March 30th, 2019\n")




# DOWNLOAD WEBPAGE

# Downloads the webpage
billboard = requests.get("https://www.billboard.com/charts/")

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

# Ensure valid input
categorySelection = input("Select a category below by its listed number: ")
while True:
	if categorySelection.isdigit() and 1 <= int(categorySelection) <= numberOfCategories:
		categorySelection = int(categorySelection) - 1
		break
	categorySelection = input("Please enter a valid selection (numbers 1 - " + str(numberOfCategories) + "): ")




# CHART SELECTION

charts = webpage.find(id=categoriesList[categorySelection].replace(' ','').lower() + 'ChartPanel').find_all(class_="chart-panel__text")

chartsList = []
for tag in charts:
	chartsList.append(' '.join(''.join(tag.contents).split()))

numberOfCharts = len(charts)

# Show list of categories and take in a selection input
print("List of Charts:")
for i in range(numberOfCharts):
	print(i + 1, ") ", chartsList[i], sep='')
print()

# Ensure valid input
chartSelection = input("Select a chart below by its listed number: ")
while True:
	if chartSelection.isdigit() and 1 <= int(chartSelection) <= numberOfCharts:
		chartSelection = int(chartSelection) - 1
		break
	chartSelection = input("Please enter a valid selection (numbers 1 - " + str(numberOfCharts) + "): ")

print("You selected", categoriesList[categorySelection], "and", chartsList[chartSelection])




# START YEAR SELECTION

print("Enter the dates you would like to parse from:")

# Ensure valid input
startYear = input("Start Year: ")
while True:
	if startYear.isdigit() and 1958 <= int(startYear) <= datetime.now().year:
		startYear = int(startYear)
		break;
	startYear = input("Please enter a valid year (1958 - " + startYear + "): ")


















































