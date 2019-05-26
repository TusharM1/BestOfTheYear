from billboard import BillboardParser

print("Billboard Chart Parser v2.1")
print("This tool will scrape the Billboard website to find the best songs and lookup their Spotify IDs")
print("All charts are available for parsing but some may not work as they are not time based or of songs")
print("Barely working as of May 21st, 2019\n")

billboard_parser = BillboardParser()

print("Please select a category from the list:")
categories = billboard_parser.get_categories()
for i in range(len(categories)):
    print(i + 1, ") ", categories[i], sep='')
print()

category_selection = input("Category number: ")
while True:
    if category_selection.isdigit() and 1 <= int(category_selection) <= len(categories):
        category_selection = int(category_selection) - 1
        break
    category_selection = input("Please enter a valid selection (numbers 1 - %d): " % len(categories))

print("Please select a chart from the list:")
charts = billboard_parser.get_charts(categories[category_selection])
for i in range(len(charts)):
    print(i + 1, ") ", charts[i], sep='')
print()

chart_selection = input("Chart number: ")
while True:
    if chart_selection.isdigit() and 1 <= int(chart_selection) <= len(charts):
        chart_selection = int(chart_selection) - 1
        break
    chart_selection = input("Please enter a valid selection (numbers 1 - %d): " % len(charts))

print("Enter the dates you would like to parse from:")

while True:
    print("Starting Date: ", end="")
    while True:
        try:
            starting_date = billboard_parser.get_nearest_valid_date(input())
            break
        except Exception:
            print("Please enter a valid date: ", end="")
    print("Ending Date: ", end="")
    while True:
        try:
            ending_date = billboard_parser.get_nearest_valid_date(input())
            break
        except Exception:
            print("Please enter a valid date: ", end="")
    if starting_date <= ending_date:
        break
    print("Starting Date ({}) must be before the ending date ({})".format(str(starting_date.date()),
                                                                          str(ending_date.date())))

max_size = input("Enter the maximum desired entries (or leave blank for no maximum): ")
while True:
    if max_size.isdigit() and int(max_size) >= 0:
        max_size = int(max_size)
        break
    max_size = input("Please enter a valid number greater than 0: ")

retrieve_spotify_ids = input("Retrieve Spotify IDs for songs? (Yes / No): ")
while True:
    retrieve_spotify_ids = retrieve_spotify_ids.lower()
    if retrieve_spotify_ids == 'yes' or retrieve_spotify_ids == 'y':
        retrieve_spotify_ids = True
        break
    if retrieve_spotify_ids == 'no' or retrieve_spotify_ids == 'n':
        retrieve_spotify_ids = False
        break
    retrieve_spotify_ids = input("Please enter either Yes or No: ")
print()
best_songs = billboard_parser.parse(categories[category_selection], charts[chart_selection],
                                    starting_date, ending_date, max_size, retrieve_spotify_ids)

for rank in range(min(len(best_songs), 100)):
    song_output = str(rank + 1) + ") "
    try:
        song_output += best_songs[rank]['artistName']
        if best_songs[rank]['songTitle'] != '':
            song_output += " - " + best_songs[rank]['songTitle']
        if retrieve_spotify_ids:
            if best_songs[rank]['spotifyID'] != '':
                song_output += " - " + best_songs[rank]['spotifyID']
    except Exception:
        song_output = "ERROR: " + best_songs[rank]['artistName'] + " - " + best_songs[rank]['songTitle']
    print(song_output)
