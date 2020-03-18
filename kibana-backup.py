#!/usr/bin/env python3

# Kibana documentation:
# https://www.elastic.co/guide/en/kibana/current/saved-objects-api-export.html
# https://www.elastic.co/guide/en/kibana/current/saved-objects-api-import.html

import sys
import argparse
import requests

# Error message from Kibana listing all possible saved objects types:
# \"type\" must be one of [config, map, canvas-workpad, canvas-element, index-pattern, visualization, search, dashboard, url]
saved_objects_types = (
    'config', 'map', 'canvas-workpad', 'canvas-element', 'index-pattern',
    'visualization', 'search', 'dashboard', 'url')


def backup(kibana_url, user, password):
    """Return string with newline-delimitered json containing Kibana saved objects"""
    saved_objects = {}
    url = kibana_url + '/api/saved_objects/_export'
    for obj_type in saved_objects_types:
        # print(obj_type)
        r = requests.post(
            url,
            auth=(user, password),
            headers={'Content-Type': 'application/json', 'kbn-xsrf': 'reporting'},
            data='{ "type": "' + obj_type + '" }'
        )
        r.raise_for_status()  # Raises stored HTTPError, if one occurred.
        saved_objects[obj_type] = r.text

    return '\n'.join(saved_objects.values())


def restore(kibana_url, user, password, text):
    """Restore given newline-delimitered json containing saved objects to Kibana"""

    url = kibana_url + '/api/saved_objects/_import?overwrite=true'
    print('POST ' + url)
    r = requests.post(
        url,
        auth=(user, password),
        headers={'kbn-xsrf': 'reporting'},
        files={'file': ('backup.ndjson', text)}
    )

    print(r.status_code, r.reason, '\n', r.text)
    r.raise_for_status()  # Raises stored HTTPError, if one occurred.


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(
        description='Backup and restore Kibana saved objects. Writes backup to stdout and reads from stdin.'
    )
    args_parser.add_argument('action', choices=['backup', 'restore'])
    args_parser.add_argument('--kibana-url', default='http://127.0.0.1:5601', help='URL to access Kibana API')
    args_parser.add_argument('--user', default='', help='Kibana user')
    args_parser.add_argument('--password', default='', help='Kibana password')
    args = args_parser.parse_args()

    if args.action == 'backup':
        print(backup(args.kibana_url, args.user, args.password))
    elif args.action == 'restore':
        restore(args.kibana_url, args.user, args.password, ''.join(sys.stdin.readlines()))
