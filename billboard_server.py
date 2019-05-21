#!flask/bin/python
from flask import Flask, jsonify, request, json
from billboard import BillboardParser

app = Flask(__name__)

billboard_parser = BillboardParser()

@app.route('/get-all-charts/')
def get_categories():
	return json.dumps(billboard_parser.get_all_charts()), 200, {'Content-Type': 'application/json'}

@app.route('/billboard-parser/')
def parse():
	category = request.args.get('category')
	chart = request.args.get('chart')
	starting_date = billboard_parser.get_nearest_valid_date(request.args.get('starting-date'))
	ending_date = billboard_parser.get_nearest_valid_date(request.args.get('ending-date'))
	max_size = request.args.get('max-size')
	require_spotify_ids = request.args.get('require-spotify-ids')
	return json.dumps(billboard_parser.parse(category, chart, starting_date, ending_date, max_size, require_spotify_ids)), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True)