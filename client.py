import flask
from flask import request
import argparse
import requests
from datetime import datetime
parser = argparse.ArgumentParser()

subs = parser.add_subparsers()
add_parser = subs.add_parser('add_new_trip')
update_parser = subs.add_parser('update_trip')
delete_parser = subs.add_parser('delete_trip')
find_parser = subs.add_parser('find_trip')
show_parser = subs.add_parser('show_trip')

add_parser.set_defaults(method='add')
update_parser.set_defaults(method='update')
delete_parser.set_defaults(method='delete')
find_parser.set_defaults(method='find')
show_parser.set_defaults(method='show')

add_parser.add_argument('--trip-id', required=True)
add_parser.add_argument('--city', required=True)
add_parser.add_argument('--departure', required=True,
                        help="The first day - format DD/MM/YYYY",
                        type=lambda s: datetime.strptime(s, '%d/%m/%Y'))
add_parser.add_argument('--arrival', required=True,
                        help="The last day - format DD/MM/YYYY",
                        type=lambda s: datetime.strptime(s, '%d/%m/%Y'))

update_parser.add_argument('--trip-id', required=True)
update_parser.add_argument('--city')
update_parser.add_argument('--departure',
                           help="The first day - format DD/MM/YYYY",
                           type=lambda s: datetime.strptime(s, '%d/%m/%Y'))
update_parser.add_argument('--arrival',
                           help="The last day - format DD/MM/YYYY",
                           type=lambda s: datetime.strptime(s, '%d/%m/%Y'))

delete_parser.add_argument('--trip-id', required=True)

show_parser.add_argument('--trip-id', required=True)

find_parser.add_argument('--city')
find_parser.add_argument('--departure',
                         help="The first day - format DD/MM/YYYY",
                         type=lambda s: datetime.strptime(s, '%d/%m/%Y'))
find_parser.add_argument('--arrival',
                         help='The last day - format DD/MM/YYYY',
                         type=lambda s: datetime.strptime(s, '%d/%m/%Y'))

args = parser.parse_args()
if args.method == 'add':
    parameters = {'id': args.trip_id, 'city': args.city,
                  'departure': args.departure, 'arrival': args.arrival}
    result = requests.post('http://localhost:50001/add_trip', data=parameters)
    print(result.content)
elif args.method == 'show':
    parameters = {'id': args.trip_id}
    result = requests.get('http://localhost:50001/show_trip', data=parameters)
    print(result.content)
elif args.method == 'update':
    parameters = {'id': args.trip_id}
    if args.departure is not None:
        parameters['city'] = args.city
    else:
        parameters['city'] = 'Not given'
    if args.arrival is not None:
        parameters['arrival'] = args.arrival
    else:
        parameters['arrival'] = 'Not given'
    if args.departure is not None:
        parameters['departure'] = args.departure
    else:
        parameters['departure'] = 'Not given'
    result = requests.post('http://localhost:50001/update_trip', data=parameters)
    print(result.content)
elif args.method == 'delete':
    parameters = {'id': args.trip_id}
    result = requests.post('http://localhost:50001/delete_trip', data=parameters)
    print(result.content)
elif args.method == 'find':
    parameters = {}
    if args.departure is not None:
        parameters['city'] = args.city
    else:
        parameters['city'] = 'Not given'
    if args.arrival is not None:
        parameters['arrival'] = args.arrival
    else:
        parameters['arrival'] = 'Not given'
    if args.departure is not None:
        parameters['departure'] = args.departure
    else:
        parameters['departure'] = 'Not given'
    result = requests.get('http://localhost:50001/find_trip', data=parameters)
    print(result.content)
