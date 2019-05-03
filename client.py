from billboard import BillboardParser

print("Billboard Chart Parser v2.0")
print("This tool will parse the billboard.com website to find the best songs")
print("Working as of May 2st, 2019\n")

billboard_parser = BillboardParser()

print("Select a category from the list:")
categories = billboard_parser.get_categories()
for i in range(len(categories)): 
	print(i + 1, ") ", categories[i], sep='')
print()

category_selection = input("Category number: ")
while True:
	if category_selection.isdigit() and 1 <= int(category_selection) <= len(categories):
		category_selection = int(category_selection) - 1
		break
	category_selection = input("Please enter a valid selection (numbers 1 - %d): ", len(categories))

print("Select a chart from the list:")
charts = billboard_parser.get_charts(categories[category_selection])
for i in range(len(charts)):
	print(i + 1, ") ", charts[i], sep='')
print()

chart_selection = input("Chart number: ")
while True:
	if chart_selection.isdigit() and 1 <= int(chart_selection) <= len(charts):
		chart_selection = int(chart_selection) - 1
		break
	chart_selection = input("Please enter a valid selection (numbers 1 - " + str(len(charts)) + "): ")

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
			ending_date = print("Please enter a valid date: ", end="")
	if starting_date <= ending_date:
		break
	print("Starting Date (%s) must be before the ending date (%s)" % (str(starting_date.date()), str(ending_date.date())))	
			
best_songs = billboard_parser.parse(categories[category_selection], charts[chart_selection], starting_date, ending_date)
for rank in range(min(len(best_songs), 100)):
	print(rank + 1, ") ", best_songs[rank][1], " - ", best_songs[rank][0], sep='')