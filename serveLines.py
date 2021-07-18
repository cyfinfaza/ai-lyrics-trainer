from flask import Flask
from flask.globals import request
import json
from os import listdir
from flask_cors import CORS

from flask.wrappers import Response

app = Flask(__name__)
cors = CORS(app)

DIR = input('Dataset directory: ')

manylines: list

with open(f'{DIR}/manylines.json', encoding='utf-8') as file:
	manylines = json.loads(file.read())

if 'training.json' in listdir(DIR):
	with open(f'{DIR}/training.json', encoding='utf-8') as file:
		existing = json.loads(file.read())
else:
	with open(f'{DIR}/training.json', 'w') as file:
		file.write("[]")
	existing = []

manylines = manylines[len(existing):]

@app.route("/")
def index():
	return "server is working"

@app.route("/lineset")
def getWord():
	if len(manylines) < 1:
		return Response(json.dumps({"lines":[], "remaining":len(manylines)}), 200, content_type="application/json")
	return Response(json.dumps({"lines":manylines[0], "remaining":len(manylines)}), 200, content_type="application/json")

@app.route("/save", methods=["POST"])
def save():
	data = json.loads(request.data.decode('utf-8'))
	with open(f'{DIR}/training.json', "r") as file:
		current: list = json.loads(file.read())
	with open(f'{DIR}/training.json', 'w') as file:
		current.append(data)
		file.write(json.dumps(current))
	manylines.pop(0)
	return "ok"

@app.route("/skip")
def skip():
	manylines.pop(0)

if __name__ == "__main__":
	app.run(debug=True, port=5004)