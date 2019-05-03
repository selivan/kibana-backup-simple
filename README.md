## kibana-backup-simple

Simple backup for Kibana Saved Objects: config, index patterns, dashboards, saved searches, etc.

## Usage

`kibana-backup.py [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD] {backup,restore}`

* `backup` write backup file in json format to stdout
* `restore` restore backup from stdout
* `--kibana-url` base URL to access Kibana API, default: `http://127.0.0.1:5601`
* `--user` Kibana user
* `--password` Kibana password

## Documentation

* https://www.elastic.co/guide/en/kibana/current/saved-objects-api-get.html
* https://www.elastic.co/guide/en/kibana/current/saved-objects-api-create.html
