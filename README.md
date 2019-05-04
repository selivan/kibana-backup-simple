Simple backup for Kibana saved objects: config, index patterns, dashboards, saved searches, etc.

Uses python3 and [python-requests](https://2.python-requests.org/) library, which you have to install on your every host anyway, because it's awesome.

### Usage

`kibana-backup.py [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD] backup > backup.json`

`cat backup.json | kibana-backup.py [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD] restore`

* `backup` write backup file in json format to stdout
* `restore` restore backup from stdin
* `--kibana-url` base URL to access Kibana API, default: `http://127.0.0.1:5601`
* `--user` Kibana user
* `--password` Kibana password

### Documentation

* https://www.elastic.co/guide/en/kibana/current/saved-objects-api-get.html
* https://www.elastic.co/guide/en/kibana/current/saved-objects-api-create.html

### License

[WTFPL](LICENSE)

**P.S.** If this code is useful for you - don't forget to put a star on it's [github repo](https://github.com/selivan/kibana-backup-simple).
