import flask
import argparse
from flask import request

app = flask.Flask('client')


@app.route('/', methods=['POST', 'GET'])
def show_page():
    return 'OK'


@app.route('/add_trip', methods=['POST'])
def new_trip():
    return 'OK'


@app.route('/update_trip', methods=['POST'])
def update_trip():
    return 'OK'


@app.route('/delete_trip', methods=['POST'])
def delete_trip():
    return 'OK'


@app.route('/show_trip', methods=['GET'])
def show_trip():
    print(request.form['id'])
    return 'OK'


@app.route('/find_trip', methods=['GET'])
def find_trip():
    return 'OK'


parser = argparse.ArgumentParser()
parser.add_argument('--port', default=50001, type=int)
args = parser.parse_args()

app.run('::', args.port, debug=True, threaded=True)



