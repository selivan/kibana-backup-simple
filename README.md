[![PyPI version](https://badge.fury.io/py/kibana-backup-simple.svg)](https://badge.fury.io/py/kibana-backup-simple)

Simple backup for Kibana saved objects: config, index patterns, dashboards, saved searches, etc.

Uses python3 and awesome [python-requests](https://requests.readthedocs.io/) library.

### Usage

`kibana-backup.py backup [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD] > backup.ndjson`

`cat backup.ndjson | kibana-backup.py restore [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD]`

`kibana-backup.py backup [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD] --space-id=myspace --backup-file=myspace.ndjson`

`kibana-backup.py backup [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD] --all-spaces --backup-file-prefix=backup-`  
`# result: backup-default.ndjson backup-myspace.ndjson backup-myspace2.ndjson`

`kibana-backup.py restore [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD] --all-spaces --backup-file-prefix=backup-`  
`# restores backup-default.ndjson to space id=default, backup-myspace.ndjson to space id=myspace, ...`  


* `backup` create backup file in newline-delimitered json format
* `restore` restore backup from stdin
* `--kibana-url` base URL to access Kibana API, default: `http://127.0.0.1:5601`
* `--user` Kibana user
* `--password` Kibana password
* `--space-id` Kibana space id. If not set then the default space is used.
* `--all-spaces` Backup all spaces to separate files. Backup file name is used as prefix: `<backup file>-<space-id>.ndjson`

### Installation

From [pypi.org](https://pypi.org):

`pip install kibana-backup-simple`

Local installation:

```bash
git clone https://github.com/selivan/kibana-backup-simple.git
cd kibana-backup-simple
python setup.py install
```

Or just create a Docker image and use it:

```bash
docker build -t kibana-backup-simple .
docker run -it --rm kibana-backup-simple [options]
```

### Documentation

* https://www.elastic.co/guide/en/kibana/current/saved-objects-api-export.html
* https://www.elastic.co/guide/en/kibana/current/saved-objects-api-import.html
* https://www.elastic.co/guide/en/kibana/current/spaces-api-get-all.html

### License

[WTFPL](LICENSE)

**P.S.** If this code is useful for you - don't forget to put a star on it's [github repo](https://github.com/selivan/kibana-backup-simple).
