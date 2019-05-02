import json
import argparse
import requests
from datetime import datetime

start_parser = argparse.ArgumentParser()

start_parser.add_argument('--host', default='localhost')
start_parser.add_argument('--port', default=50001, type=int)

parser = argparse.ArgumentParser()

subs = parser.add_subparsers()
exit_parser = subs.add_parser('exit')
add_parser = subs.add_parser('add_new_trip')
update_parser = subs.add_parser('update_trip')
delete_parser = subs.add_parser('delete_trip')
find_parser = subs.add_parser('find_trip')
show_parser = subs.add_parser('show_trip')

exit_parser.set_defaults(method='exit')
add_parser.set_defaults(method='add')
update_parser.set_defaults(method='update')
delete_parser.set_defaults(method='delete')
find_parser.set_defaults(method='find')
show_parser.set_defaults(method='show')

add_parser.add_argument('--trip-id', required=True)
add_parser.add_argument('--city', required=True)
add_parser.add_argument('--departure', required=True,
                        help='The first day - format DD/MM/YYYY',
                        type=lambda s: datetime.strptime(s, '%d/%m/%Y').date())
add_parser.add_argument('--arrival', required=True,
                        help='The last day - format DD/MM/YYYY',
                        type=lambda s: datetime.strptime(s, '%d/%m/%Y').date())

update_parser.add_argument('--trip-id', required=True)
update_parser.add_argument('--city')
update_parser.add_argument('--departure',
                           help='The first day - format DD/MM/YYYY',
                           type=lambda s: datetime.strptime(s, '%d/%m/%Y').date())
update_parser.add_argument('--arrival',
                           help='The last day - format DD/MM/YYYY',
                           type=lambda s: datetime.strptime(s, '%d/%m/%Y').date())

delete_parser.add_argument('--trip-id', required=True)

show_parser.add_argument('--trip-id', required=True)

find_parser.add_argument('--city', help='Destination')
find_parser.add_argument('--departure',
                         help='The first day - format DD/MM/YYYY',
                         type=lambda s: datetime.strptime(s, '%d/%m/%Y').date())
find_parser.add_argument('--arrival',
                         help='The last day - format DD/MM/YYYY',
                         type=lambda s: datetime.strptime(s, '%d/%m/%Y').date())


start_args = start_parser.parse_args()
host = start_args.host
port = start_args.port
while True:
    input_line = input().split()
    args = parser.parse_args(input_line)
    if args.method == 'exit':
        break
    if args.method == 'add':
        parameters = {'id': args.trip_id, 'city': args.city,
                      'departure': args.departure, 'arrival': args.arrival}
        result = requests.post('http://{}:{}/add_trip'.format(host, port),
                               data=parameters)
        print(result.text)
    elif args.method == 'show':
        parameters = {'id': args.trip_id}
        result = requests.get('http://{}:{}/show_trip'.format(host, port),
                              data=parameters)
        try:
            result = json.loads(result.content)
            keys = ('trip_id', 'city', 'departure', 'arrival')
            for key in keys:
                print(key, result[key])
        except:
            print(result.text)
    elif args.method == 'update':
        parameters = {'id': args.trip_id, 'city': args.city,
                      'departure': args.departure, 'arrival': args.arrival}
        result = requests.post('http://{}:{}/update_trip'.format(host, port),
                               data=parameters)
        print(result.text)
    elif args.method == 'delete':
        parameters = {'id': args.trip_id}
        result = requests.post('http://{}:{}/delete_trip'.format(host, port),
                               data=parameters)
        print(result.text)
    elif args.method == 'find':
        parameters = {'city': args.city, 'departure': args.departure,
                      'arrival': args.arrival}
        result = requests.get('http://{}:{}/find_trip'.format(host, port),
                              data=parameters)
        try:
            result = json.loads(result.content)
            for value in result.values():
                print('\ntrip id  {}\ncity  {}\ndeparture {}\narrival {}'.format(
                    value[0], value[1], value[2], value[3]))
        except:
            print(result.text)
