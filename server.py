from flask import Flask, request, abort
from time import time


app = Flask(__name__)
db = []

@app.route('/')
def index():
	return '<a href="/status">STATUS</a>'

@app.route('/status')
def status():
	return {'status': True,
			'name': 'Messenger',
			'time': str(time()),
			'messages_count': len(db),
			'users_count': len(set(message['name'] for message in db))
			}



@app.route('/send', methods = ['POST'])
def send():
	data = request.json

	timestamp = time()
	db.append({
		'id': len(db),
		'name': data['name'],
		'text': data['text'],
		'timestamp': timestamp
	})
	return {'ok': True}


@app.route('/messages')
def messages():
	if 'after_timestamp' in request.args:
		after_timestamp = float(request.args['after_timestamp'])
	else:
		after_timestamp = 0

	max_limit = 100
	if 'limit' in request.args:
		limit = int(request.args['limit'])
		if limit > max_limit:
			abort(400, "too big limit")
	else:
		limit = max_limit


	after_id = 0
	for message in db:
		if message['timestamp'] > after_timestamp:
			break
		after_id += 1

	return {'messages': db[after_id:after_id+limit]}


app.run()