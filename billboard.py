import requests
from bs4 import BeautifulSoup
import re
import dateparser
from datetime import datetime, timedelta, date

class BillboardParser:

	def __init__(self):
		self.billboard_URL = "https://www.billboard.com"
		self.todays_date = datetime.now().date()
		self.all_charts = dict()
		try :
			# charts_webpage = BeautifulSoup(requests.get(self.billboard_URL + "/charts/").text, 'html.parser')
			charts_webpage = BeautifulSoup(open('index.html', 'r').read(), 'html.parser')
		except Exception:
			raise Exception("Unfortunately, something went wrong. Did the Billboard website change? (Error Code: 0)")
		try:
			for category in charts_webpage.select('.chart-panel__item.chart-panel__item--selector'):
				current_category = ' '.join(''.join(category.div.contents).split())
				self.all_charts[current_category] = dict()
				for chart in charts_webpage.find_all(id=re.sub('[ /&]', '', current_category).lower() + 'ChartPanel'):
					chart_names = [' '.join(''.join(chart_link.contents).split()) for chart_link in chart.find_all(class_="chart-panel__text")]
					chart_links = [chart_name['href'] for chart_name in chart.find_all('a')]
					for chart in range(len(chart_names)):
						self.all_charts[current_category][chart_names[chart]] = chart_links[chart]
					# self.all_charts[current_category].append([' '.join(''.join(chart.find(class_="chart-panel__text").contents).split()), chart.find_all('a')['href']])
				# self.all_charts[current_category] = [chart.find('a')['href'], ' '.join(''.join(chart.find_all(class_="chart-panel__text").contents).split())]
				# for chart in charts_webpage.find(id=re.sub('[ /&]', '', current_category).lower() + 'ChartPanel')
				# print(filter(lambda x: x != '\n', charts_webpage.find(id=re.sub('[ /&]', '', current_category).lower() + 'ChartPanel')))
				# for chart in charts_webpage.find(id=re.sub('[ /&]', '', current_category).lower() + 'ChartPanel'):
				# 	# print(chart.contents)
					# self.all_charts[current_category] = [chart['href'], ' '.join(''.join(chart.find_all(class_="chart-panel__text").contents).split())]
				# # self.all_charts[current_category].append(re.sub('[ /&]', '', ''.join(self.all_charts[current_category][0])))
				# # print(self.all_charts[current_category][1])
		except Exception as e:
			raise e
			# print(e)
			# pass
		
	def get_categories(self):
		return list(self.all_charts.keys())

	def get_charts(self, category):
		return list(self.all_charts[category].keys())

	def get_nearest_valid_date(self, current_date):
		nearest_date = dateparser.parse(current_date).date()
		nearest_date += timedelta(days=((5 - nearest_date.weekday()) % 7))
		if nearest_date > self.todays_date:
			nearest_date -= timedelta(days=7)
		return max(min(nearest_date, self.todays_date), date(1958, 7, 28))

	def parse(self, category, chart, starting_date, ending_date):
		try:
			def download(current_date):
				print("Currently parsing " + str(current_date))
				# print(self.all_charts[chart].parent.parent['href'])
				print(self.billboard_URL + self.all_charts[category][chart] + '/' + str(current_date))
				return BeautifulSoup(requests.get(self.billboard_URL + self.all_charts[category][chart] + '/' + str(current_date)).text, 'html.parser')
			def get_song_list(current_webpage):
				song_dictionary = {}
				song_blocks = current_webpage.select(".chart-list.chart-details__left-rail")
				for song_block in song_blocks:
					song_list = song_block.find_all("div", "chart-list-item")
					for song in song_list:
						song_key = (song['data-artist'], song['data-title'])
						rank_value = len(song_blocks) * len(song_list) + 1 - int(song['data-rank'])
						song_dictionary[song_key] = rank_value
				return song_dictionary
			def get_next_date():
				current_URL = self.billboard_URL + current_webpage.select('.dropdown__date-selector-option')[1].a['href']
				return dateparser.parse(current_URL[-10:]).date()	
			current_webpage = download(starting_date)
			song_dictionary = get_song_list(current_webpage)
			while True:
				current_date = get_next_date()
				if current_date == None or current_date > ending_date:
					break
				current_webpage = download(current_date)
				current_dictionary = get_song_list(current_webpage)
				for key in current_dictionary:
					song_dictionary[key] = song_dictionary.get(key, 0) + current_dictionary[key]
			best_songs = sorted(song_dictionary, key=song_dictionary.get)
			best_songs.reverse()
			return best_songs
		except Exception:
			raise Exception('Something went very wrong...')
				