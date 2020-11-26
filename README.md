[![pypi 20package](https://img.shields.io/pypi/v/kibana-backup-simple?color=%233fb911&label=pypi%20package)](https://pypi.org/project/kibana-backup-simple/)

Simple backup for Kibana saved objects: config, index patterns, dashboards, saved searches, etc.

Uses python3 and awesome [python-requests](https://requests.readthedocs.io/) library.

### Usage

#### Backup/restore default namespace

`kibana-backup.py backup [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD] > backup.ndjson`

`cat backup.ndjson | kibana-backup.py restore [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD]`

#### Backup non-default namespace

`kibana-backup.py backup [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD] --space-id=myspace --backup-file=myspace.ndjson`

#### Backup/restore all namespaces

`kibana-backup.py backup [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD] --all-spaces --backup-file-prefix=backup-`  
  
Result: `backup-default.ndjson backup-myspace.ndjson backup-myspace2.ndjson`  

`kibana-backup.py restore [--kibana-url KIBANA_URL] [--user USER] [--password PASSWORD] --all-spaces --backup-file-prefix=backup-`  
  
Restores `backup-default.ndjson` to space `id=default`, `backup-myspace.ndjson` to space `id=myspace`, ...  

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
