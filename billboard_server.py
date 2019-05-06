#!flask/bin/python
from flask import Flask, jsonify, request
from billboard import BillboardParser

app = Flask(__name__)	

billboard_parser = BillboardParser()

@app.route('/get-all-charts/')
def get_categories():
	return jsonify(billboard_parser.get_all_charts())

@app.route('/billboard-parser/')
def parse():
	category = request.args.get('category')
	chart = request.args.get('chart')
	starting_date = billboard_parser.get_nearest_valid_date(request.args.get('starting-date'))
	ending_date = billboard_parser.get_nearest_valid_date(request.args.get('ending-date'))
	require_spotify_ids = request.args.get('require-spotify-ids')
	return jsonify(billboard_parser.parse(category, chart, starting_date, ending_date, require_spotify_ids))

if __name__ == '__main__':
    app.run(debug=True)