FROM python:3-slim

COPY *.py *.md VERSION LICENSE /opt/

WORKDIR /opt

RUN python setup.py install

ENTRYPOINT ["/usr/local/bin/kibana-backup.py"]

CMD ["--help"]
