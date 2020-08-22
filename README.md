Simple backup for Kibana saved objects: config, index patterns, dashboards, saved searches, etc.

Uses python3 and [python-requests](https://requests.readthedocs.io/) library, which you have to install on your every host anyway, because it's awesome.

### Usage
Backup
```console
kibana-backup.py [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD] [--file-name FILENAME] backup
```

Restore
```console
kibana-backup.py [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD] [--file-name FILENAME] restore
```

If you want to store backup data in S3 you need to specify environments variable AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_ID. More info [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)

* `backup` write backup file in newline-delimitered json format to stdout
* `restore` restore backup from stdin
* `--kibana-url` base URL to access Kibana API, default: `http://127.0.0.1:5601`
* `--space-id` Kibana space id. If not set then the default space is used.
* `--user` Kibana user
* `--password` Kibana password
* `--s3-bucket` Bucket name to save or restore a backup file
* `--file-name` Name of a file to save backup

 *Note:* To use the default space you should not set `--space-id` parameter. Setting it to the default space id: `default` does not work.
 

### Documentation

* https://www.elastic.co/guide/en/kibana/current/saved-objects-api-export.html
* https://www.elastic.co/guide/en/kibana/current/saved-objects-api-import.html

### License

[WTFPL](LICENSE)

**P.S.** If this code is useful for you - don't forget to put a star on it's [github repo](https://github.com/selivan/kibana-backup-simple).
