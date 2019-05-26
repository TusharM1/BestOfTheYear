import requests
from bs4 import BeautifulSoup
import re
import dateparser
from datetime import datetime, timedelta, date
import spotipy
from spotipy import oauth2 as auth
import yaml


class BillboardParser:

    def __init__(self):
        self.billboard_URL = "https://www.billboard.com"
        self.todays_date = datetime.now().date()
        self.all_charts = dict()
        try:
            charts_webpage = BeautifulSoup(requests.get(self.billboard_URL + "/charts/").text, 'html.parser')
            for category in charts_webpage.select('.chart-panel__item.chart-panel__item--selector'):
                current_category = ' '.join(''.join(category.div.contents).split())
                for chart in charts_webpage.find_all(id=re.sub('[ /&]', '', current_category).lower() + 'ChartPanel'):
                    self.all_charts[current_category] = dict(zip(
                        [' '.join(''.join(chart_link.contents).split()) for chart_link in
                         chart.find_all(class_="chart-panel__text")],
                        [chart_name['href'] for chart_name in chart.find_all('a')]))
        except Exception:
            raise Exception("Unfortunately, something went wrong. Did the Billboard website change?")

    def get_categories(self):
        return list(self.all_charts.keys())

    def get_charts(self, category):
        return list(self.all_charts[category].keys())

    def get_all_charts(self):
        return dict(zip(self.all_charts.keys(), [list(value.keys()) for value in self.all_charts.values()]))

    def get_nearest_valid_date(self, current_date):
        nearest_date = dateparser.parse(current_date).date()
        nearest_date += timedelta(days=((5 - nearest_date.weekday()) % 7))
        if nearest_date > self.todays_date:
            nearest_date -= timedelta(days=7)
        return max(min(nearest_date, self.todays_date), date(1958, 7, 28))

    def parse(self, category, chart, starting_date, ending_date, max_size, retrieve_spotify_ids):
        try:
            def download(current_date):
                print("Parsing " + self.billboard_URL + self.all_charts[category][chart] + '/' + str(current_date))
                return BeautifulSoup(
                    requests.get(self.billboard_URL + self.all_charts[category][chart] + '/' + str(current_date)).text,
                    'html.parser')

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
                try:
                    current_url = self.billboard_URL + current_webpage.select('.dropdown__date-selector-option')[1].a[
                        'href']
                    return dateparser.parse(current_url[-10:]).date()
                except Exception:
                    return None

            print()
            # TODO Fix this for charts like Greatest of All Time that don't have dates
            current_webpage = download(starting_date)
            song_dictionary = get_song_list(current_webpage)
            while True:
                current_date = get_next_date()
                if current_date is None or current_date > ending_date:
                    break
                current_webpage = download(current_date)
                current_dictionary = get_song_list(current_webpage)
                for key in current_dictionary:
                    song_dictionary[key] = song_dictionary.get(key, 0) + current_dictionary[key]
            print()
            best_songs = sorted(song_dictionary, key=song_dictionary.get)
            best_songs.reverse()
            best_songs = [dict(zip(['artistName', 'songTitle'], song)) for song in best_songs]
            if type(max_size) is str:
                max_size = re.sub('[\"\']', '', max_size)
                if max_size.isdigit():
                    max_size = int(max_size)
                else:
                    max_size = 0
            if max_size > 0:
                del best_songs[int(max_size):]
            retrieve_spotify_ids = re.sub('[\"\']', '', str(retrieve_spotify_ids))
            if retrieve_spotify_ids == 'True':
                print('Getting Spotify IDs...')
                credentials = yaml.safe_load(open('credentials.yml'))
                CLIENT_ID = credentials['SPOTIFY']['CLIENT_ID']
                CLIENT_SECRET = credentials['SPOTIFY']['CLIENT_SECRET']
                spotify = spotipy.Spotify(
                    auth.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET).get_access_token())
                for song in best_songs:
                    try:
                        result = spotify.search(
                            re.sub(r'([Ww]ith |[Ff]eaturing |[Xx&] | \w\*+\w|\w\*+\w )', '', song['artistName']) + " " +
                            song['songTitle'], limit=1, offset=0, type='track')
                        song['spotifyID'] = result['tracks']['items'][0]['uri']
                    except Exception:
                        print('Couldn\'t find song:', song['artistName'], '-', song['songTitle'])
            return best_songs
        except Exception:
            return []
