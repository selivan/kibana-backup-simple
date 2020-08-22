#!/usr/bin/env python3

# Kibana documentation:
# https://www.elastic.co/guide/en/kibana/current/saved-objects-api-export.html
# https://www.elastic.co/guide/en/kibana/current/saved-objects-api-import.html

import sys
import argparse
import requests
import boto3
import json

# Error message from Kibana listing all possible saved objects types: \"type\" must be one of [config, map,
# canvas-workpad, canvas-element, index-pattern, visualization, search, dashboard, url]
saved_objects_types = (
    'config', 'map', 'canvas-workpad', 'canvas-element', 'index-pattern',
    'visualization', 'search', 'dashboard', 'url')


class Amazon:
    def __init__(self):
        self.s3 = self.s3_conn()

    def s3_conn(self):
        try:
            s3 = boto3.client('s3')
        except Exception as err:
            raise Exception(f'Failed in S3 connection, environments to aws are defined?: {err}')
        return s3

    def upload_backup(self, fileobj, bucket, file_name):
        try:
            self.s3.put_object(Body=fileobj, Bucket=bucket, Key=file_name)
        except Exception as err:
            raise Exception(f'Failed in upload file: {err}')

    def get_backup(self, bucket, file_name, tmp_location):
        try:
            with open(tmp_location, 'wb') as f:
                self.s3.download_fileobj(bucket, file_name, f)
        except Exception as err:
            raise Exception(f'Failed in get file: {err}')


class Action:
    def __init__(self, kibana_url, space_id, kibana_user, kibana_password, bucket, file_name):
        self.kibana_url = kibana_url
        self.space_id = space_id
        self.kibana_user = kibana_user
        self.kibana_password = kibana_password
        self.bucket = bucket
        self.file_name = file_name
        if not file_name:
            self.file_name = 'kibana-default-backup.json'

    def backup(self):
        """Return string with newline-delimitered json containing Kibana saved objects"""
        saved_objects = {}
        if len(self.space_id):
            url = self.kibana_url + '/s/' + self.space_id + '/api/saved_objects/_export'
        else:
            url = self.kibana_url + '/api/saved_objects/_export'
        for obj_type in saved_objects_types:
            # print(obj_type)
            r = requests.post(
                url,
                auth=(self.kibana_user, self.kibana_password),
                headers={'Content-Type': 'application/json', 'kbn-xsrf': 'reporting'},
                data='{ "type": "' + obj_type + '" }'
            )
            r.raise_for_status()  # Raises stored HTTPError, if one occurred.
            saved_objects[obj_type] = r.text

        full_file = '\n'.join(saved_objects.values())

        if self.bucket:
            aws = Amazon()
            aws.upload_backup(full_file.encode(), self.bucket, self.file_name)

            full_file = f'File uploaded with name {self.file_name} to {self.bucket}:\n {full_file}'

        with open(self.file_name, 'w') as backup_file:
            print(json.dumps(backup_file, indent=4))
        return full_file

    def restore(self):
        """Restore given newline-delimitered json containing saved objects to Kibana"""

        if len(self.space_id):
            url = self.kibana_url + '/s/' + self.space_id + '/api/saved_objects/_import?overwrite=true'
        else:
            url = self.kibana_url + '/api/saved_objects/_import?overwrite=true'

        file_to_post = self.file_name

        if self.bucket:
            tmp_location = f'/tmp/{self.file_name}'
            aws = Amazon()
            aws.get_backup(self.bucket, self.file_name, tmp_location)
            file_to_post = tmp_location

        if sys.stdin.readlines():
            text = ''.join(sys.stdin.readlines())
            file_to_post = (self.file_name, text)

        print('POST ' + url)
        r = requests.post(
            url,
            auth=(self.kibana_user, self.kibana_password),
            headers={'kbn-xsrf': 'reporting'},
            files={'file': file_to_post}
        )

        print(r.status_code, r.reason, '\n', r.text)
        r.raise_for_status()  # Raises stored HTTPError, if one occurred.


def default_parser():
    args_parser = argparse.ArgumentParser(
        description='Backup and restore Kibana saved objects. Writes backup to a file local or in s3 and reads from '
                    'then. '
    )
    subparser = args_parser.add_subparsers(help="Using backup or restore", dest='command')

    subparser.add_parser('backup')

    subparser.add_parser('restore')

    # Default options
    args_parser.add_argument('--s3-bucket', default='', help='S3 bucket name')
    args_parser.add_argument('--file-name', default='', help='File name to store or to be restor')
    args_parser.add_argument('--kibana-url', default='http://127.0.0.1:5601', help='URL to access Kibana API')
    args_parser.add_argument('--space-id', default='',
                             help='Kibana space id. If not set then the default space is used.')
    args_parser.add_argument('--user', default='', help='Kibana user')
    args_parser.add_argument('--password', default='', help='Kibana password')
    args = args_parser.parse_args()

    return args


if __name__ == '__main__':
    args = default_parser()
    act = Action(args.kibana_url, args.space_id, args.user, args.password, args.s3_bucket, args.file_name)

    if args.command == 'backup':
        response = act.backup()
        print(response)
    elif args.command == 'restore':
        act.restore()
