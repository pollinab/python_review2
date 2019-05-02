import flask
import argparse
from flask import request
import sqlite3

app = flask.Flask('client')

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE if not exists trips
                  (trip_id text, city text, departure text,
                   arrival text)
               """)


@app.route('/add_trip', methods=['POST'])
def new_trip():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT trip_id FROM trips WHERE trip_id = ?",
                   [request.form['id']])
    if cursor.fetchone() is None:
        trip = (request.form['id'], request.form['city'],
                request.form['departure'], request.form['arrival'])
        cursor.execute("INSERT INTO trips VALUES (?, ?, ?, ?)", trip)
        conn.commit()
        conn.close()
        return 'OK'
    conn.close()
    return 'ERROR: this id already exists'


@app.route('/update_trip', methods=['POST'])
def update_trip():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT trip_id FROM trips WHERE trip_id = ?",
                   [request.form['id']])
    if cursor.fetchone() is None:
        return 'ERROR: id not found'
    if request.form.get('city') is not None:
        cursor.execute("UPDATE trips SET city = ? WHERE trip_id = ?",
                       (request.form['city'], request.form['id']))
    if request.form.get('departure') is not None:
        cursor.execute("UPDATE trips SET departure = ? WHERE trip_id = ?",
                       (request.form['departure'], request.form['id']))
    if request.form.get('arrival') is not None:
        cursor.execute("UPDATE trips SET arrival = ? WHERE trip_id = ?",
                       (request.form['arrival'], request.form['id']))
    conn.commit()
    conn.close()
    return 'OK'


@app.route('/delete_trip', methods=['POST'])
def delete_trip():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trips WHERE trip_id = ?",
                   [request.form['id']])
    conn.commit()
    conn.close()
    return 'OK'


@app.route('/show_trip', methods=['GET'])
def show_trip():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trips WHERE trip_id = ?",
                   [request.form['id']])
    trip = cursor.fetchone()
    conn.close()
    if trip is None:
        return 'ERROR: id not found'
    keys = ('trip_id', 'city', 'departure', 'arrival')
    return flask.jsonify(dict(zip(keys, trip)))


@app.route('/find_trip', methods=['GET'])
def find_trip():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    c = request.form.get('city')
    d = request.form.get('departure')
    a = request.form.get('arrival')
    cursor.execute("""SELECT * FROM trips 
                    WHERE (? IS NULL OR city = ?)
                    AND (? IS NULL OR departure = ?)
                    AND (? IS NULL OR arrival = ?)""",
                   (c, c, d, d, a, a))
    trips = cursor.fetchall()
    conn.close()
    if not trips:
        return 'Not found'
    length = len(trips)
    return flask.jsonify({i: trips[i] for i in range(length)})


parser = argparse.ArgumentParser()
parser.add_argument('--host', default='localhost')
parser.add_argument('--port', default=50001, type=int)
args = parser.parse_args()
app.run(args.host, args.port, debug=True, threaded=True)

