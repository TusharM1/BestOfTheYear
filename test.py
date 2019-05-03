import requests
from bs4 import BeautifulSoup
import dateparser
from datetime import datetime, timedelta, date
# Get the starting month
# startDate = input("Start Month: ")
# while True:
# 	try:
# 		startDate = input("Start Month: ")
# 		startDate = dateparser.parse(startDate) + datetime.timedelta(days=(5-startDate.weekday())%7)
# 		startYear = startDate.year
# 		startMonth = startDate.month
# 		startDay = startDate.day
# 		print(startDate.day, startDate.month, startDate.year, startDate.weekday())
# 		print(startDate )	
# 	except Exception:	
# 		startDate = input("Please enter a valid date: ")

# print(startDay, startMonth, startYear)		

# startDate = input("Starting Date: ")
# print("Starting Date: ", end="")
# while True:
# 	try:
# 		startDate = dateparser.parse(input())
# 		startDate += timedelta(days=((5 - startDate.weekday()) % 7))
# 		if date(1958, 8, 4) <= startDate.date() <= datetime.now().date():
# 			break
# 		raise Exception
# 	except Exception:	
# 		startDate = print("Please enter a valid date: ", end="")

# print(startDate)		
# file = open('index.html', 'r')
# webpage = BeautifulSoup(file.read(), 'html.parser')
# charts = webpage.find(id='topchartsChartPanel').find_all(class_="chart-panel__text")

# print(charts[0].parent.parent['href'])

# url = "https://www.billboard.com/charts/hot-100/2019-01-01"

# webpage = BeautifulSoup(url, 'html.parser')

# file = open('page.html', 'r')
# file.write(webpage)
# file.write(requests.get(url).text)

# webpage = BeautifulSoup(file.read(), 'html.parser')
# print(webpage.select('.dropdown__date-selector-option')[1].a['href'])
# date = dateparser.parse(webpage.select('.dropdown__date-selector-option')[1].a['href'][-13:])
# print(webpage.select('.dropdown__date-selector-option')[1].a['href'][-10:])

# " data-rank="9" data-artist="J. Cole" data-title="Middle Child" 

# songBlocks = webpage.select(".chart-list.chart-details__left-rail")
# songs = []
# for block in songBlocks:
# 	songList = block.find_all("div", "chart-list-item")
# 	for song in songList:
# 		print(song['data-rank'], song['data-artist'], song['data-title'])

# date = dateparser.parse("january 1st 2019")
# date += timedelta(days=((5 - date.weekday()) % 7))
# endDate = dateparser.parse("february 1st 2019")
# while date < endDate:
# 	string = "%d-%02d-%02d" % (date.year, date.month, date.day)
# 	# week = BeautifulSoup(url + , 'html.parser')
# 	print(string)
# 	date += timedelta(days=7)

file = open("chart-list.json", "w")














