FROM python:3.10-slim

ENV FLASK_APP=lab

COPY requirements.txt /opt

RUN python3 -m pip install -r /opt/requirements.txt

COPY lab /opt/lab

WORKDIR /opt

CMD flask run --host 0.0.0.0 -p $PORT
