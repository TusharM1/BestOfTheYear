#!flask/bin/python
from flask import Flask, jsonify, request
import sys

app = Flask(__name__)	

@app.route('/billboard-parser/')
def get_current_user():
	if 'chart':
		pass
	argument1 = request.args.get('argument1')
	argument2 = request.args.get('argument2')
	argument3 = request.args.get('argument3')
	if request.args:
		pass
	print(request.args, file=sys.stderr)
	return jsonify(argument1=argument1, argument2=argument2, argument3=argument3)

if __name__ == '__main__':
    app.run(debug=True)