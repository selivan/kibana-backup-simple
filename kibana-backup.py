#!/usr/bin/env python3

# Kibana documentation:
# https://www.elastic.co/guide/en/kibana/current/saved-objects-api-find.html
# https://www.elastic.co/guide/en/kibana/current/saved-objects-api-create.html

import requests
import argparse
import json
import sys


def backup(kibana_url, user, password):
    """Return string with json containing Kibana saved objects"""

    # saved_object_types = ('visualization', 'dashboard', 'search', 'index-pattern', 'config', 'timelion-sheet')
    saved_object_types = ('index-pattern',)
    saved_objects = {}
    for obj_type in saved_object_types:
        r = requests.get(kibana_url + '/api/saved_objects/_find?type={}'.format(obj_type),
                         auth=(user, password))
        saved_objects[obj_type] = r.json()
    return json.dumps(saved_objects, sort_keys=True, indent=4)


def restore(kibana_url, user, password, text):
    """Restore given json containing saved objects to Kibana"""

    saved_objects = json.loads(text)
    for key, val in saved_objects.items():
        for obj in val['saved_objects']:
            obj_data = {'attributes': obj['attributes']}
            print('/api/saved_objects/{}/{}?overwrite=true'.format(key, obj['id']))
            r = requests.post(kibana_url + '/api/saved_objects/{}/{}?overwrite=true'.format(key, obj['id']),
                              auth=(user, password),
                              headers={'Content-Type': 'application/json', 'kbn-xsrf': 'reporting'},
                              data=json.dumps(obj_data))
            if r.status_code != 200:
                print(r.text)
                r.raise_for_status()  # Raises stored HTTPError, if one occurred.
            else:
                print('OK')


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(
        description='Backup and restore Kibana saved objects. Writes backup to stdout and reads from stdin.')
    args_parser.add_argument('action', choices=['backup', 'restore'])
    args_parser.add_argument('--kibana-url', default='http://127.0.0.1:5601', help='URL to access Kibana API')
    args_parser.add_argument('--user', default='', help='Kibana user')
    args_parser.add_argument('--password', default='', help='Kibana password')
    args = args_parser.parse_args()

    if args.action == 'backup':
        print(backup(args.kibana_url, args.user, args.password))
    elif args.action == 'restore':
        restore(args.kibana_url, args.user, args.password, ''.join(sys.stdin.readlines()))
