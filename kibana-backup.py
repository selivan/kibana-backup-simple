#!/usr/bin/env python3

# Kibana documentation:
# https://www.elastic.co/guide/en/kibana/current/saved-objects-api-export.html
# https://www.elastic.co/guide/en/kibana/current/saved-objects-api-import.html

import sys
import argparse
import requests
import json
import glob
import re
from collections import OrderedDict
from pprint import pprint

# Error message from Kibana listing all possible saved objects types:
# \"type\" must be one of [config, map, canvas-workpad, canvas-element, index-pattern, visualization, search, dashboard, url]
saved_objects_types = (
    'config',
    'map',
    'canvas-workpad',
    'canvas-element',
    'index-pattern',
    'visualization',
    'search',
    'dashboard',
    'url',
)


def get_all_spaces(kibana_url, user, password, verify_ssl=True):
    """Return list of all space ids in kibana, default space id goes as an empty string"""
    url = kibana_url + '/api/spaces/space'
    r = requests.get(
        url,
        auth=(user, password),
        headers={'Content-Type': 'application/json', 'kbn-xsrf': 'reporting'},
        verify=verify_ssl,
    )
    r.raise_for_status()  # Raises stored HTTPError, if one occurred.

    spaces_json = json.loads(r.text)
    spaces_list = []
    for i in spaces_json:
        if i['id'] == 'default':
            spaces_list.append('')
        else:
            spaces_list.append(i['id'])
    return spaces_list


def backup(kibana_url, space_id, user, password, verify_ssl=True):
    """Return string with newline-delimitered json containing Kibana saved objects"""
    # OrderedDict preserves items order so we have the same output if nothing changed
    saved_objects = OrderedDict()
    if len(space_id) and space_id != 'default':
        url = kibana_url + '/s/' + space_id + '/api/saved_objects/_export'
    else:
        url = kibana_url + '/api/saved_objects/_export'
    for obj_type in saved_objects_types:
        # print(obj_type)
        r = requests.post(
            url,
            auth=(user, password),
            headers={'Content-Type': 'application/json', 'kbn-xsrf': 'reporting'},
            data='{ "type": "' + obj_type + '" }',
            verify=verify_ssl,
        )
        r.raise_for_status()  # Raises stored HTTPError, if one occurred.
        saved_objects[obj_type] = r.text

    return '\n'.join(saved_objects.values())


def restore(kibana_url, space_id, user, password, text, verify_ssl=True):
    """Restore given newline-delimitered json containing saved objects to Kibana"""

    if len(space_id) and space_id != 'default':
        url = (
            kibana_url + '/s/' + space_id + '/api/saved_objects/_import?overwrite=true'
        )
    else:
        url = kibana_url + '/api/saved_objects/_import?overwrite=true'
    print('POST ' + url)
    r = requests.post(
        url,
        auth=(user, password),
        headers={'kbn-xsrf': 'reporting'},
        files={'file': ('backup.ndjson', text)},
        verify=verify_ssl,
    )

    print(r.status_code, r.reason, '\n', r.text)
    r.raise_for_status()  # Raises stored HTTPError, if one occurred.


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(
        description='Backup and restore Kibana saved objects. Writes backup to stdout or file and reads from stdin or file.'
    )
    args_parser.add_argument('action', choices=['backup', 'restore'])
    args_parser.add_argument(
        '--kibana-url',
        default='http://127.0.0.1:5601',
        help='URL to access Kibana API, default is http://127.0.0.1:5601',
    )
    args_parser.add_argument('--user', default='', help='Kibana user')
    args_parser.add_argument('--password', default='', help='Kibana password')
    args_parser.add_argument(
        '--no-verify-ssl',
        action='store_true',
        default=False,
        help='UNSAFE: Do not verify SSL/TLS certificates',
    )
    args_parser.add_argument(
        '--backup-file',
        default='',
        help='File to save or restore backup, stdout or stdin is used if not defined',
    )
    args_parser.add_argument(
        '--space-id',
        default='',
        help='Kibana space id. If not set then the default space is used.',
    )
    args_parser.add_argument(
        '--all-spaces',
        action='store_true',
        help='Backup all spaces to separate files.',
    )
    args_parser.add_argument(
        '--backup-file-prefix',
        default='',
        help='Backup file prefix for all spaces option: <prefix>-<space id>.ndjson',
    )
    args = args_parser.parse_args()

    if args.all_spaces:
        if len(args.backup_file_prefix) == 0:
            raise Exception(
                'ERROR: all spaces option requires backup file prefix to be specified'
            )
        elif args.action == 'restore':
            backup_files_wildcard = args.backup_file_prefix + '*.ndjson'
            backup_files = glob.glob(backup_files_wildcard)
            if len(backup_files) == 0:
                raise Exception(
                    'ERROR: no files like {backup_files_wildcard} were found'.format(
                        **locals()
                    )
                )
            for backup_file in backup_files:
                regexp = '{args.backup_file_prefix}(.*)\\.ndjson'.format(**locals())
                space_id = re.match(regexp, backup_file).group(1)
                if len(space_id) == 0:
                    raise Exception(
                        'File {backup_file} does not contain a valid space id'.format(
                            **locals()
                        )
                    )
                restore_content = ''.join(open(backup_file, 'r').readlines())
                restore(
                    args.kibana_url,
                    space_id,
                    args.user,
                    args.password,
                    restore_content,
                    verify_ssl=not args.no_verify_ssl,
                )
        elif args.action == 'backup':
            spaces = get_all_spaces(
                args.kibana_url,
                args.user,
                args.password,
                verify_ssl=not args.no_verify_ssl,
            )
            for space in spaces:
                backup_content = backup(
                    args.kibana_url,
                    space,
                    args.user,
                    args.password,
                    verify_ssl=not args.no_verify_ssl,
                )
                suffix = space if len(space) != 0 else 'default'
                open(
                    '{args.backup_file_prefix}{suffix}.ndjson'.format(**locals()), 'w'
                ).write(backup_content)
    else:
        if args.action == 'backup':
            backup_content = backup(
                args.kibana_url,
                args.space_id,
                args.user,
                args.password,
                verify_ssl=not args.no_verify_ssl,
            )
            if len(args.backup_file) == 0:
                print(backup_content, end='')
            else:
                open(args.backup_file, 'w').write(backup_content)
        elif args.action == 'restore':
            if len(args.backup_file) == 0:
                restore_content = ''.join(sys.stdin.readlines())
            else:
                restore_content = ''.join(open(args.backup_file, 'r').readlines())
            restore(
                args.kibana_url,
                args.space_id,
                args.user,
                args.password,
                restore_content,
                verify_ssl=not args.no_verify_ssl,
            )
