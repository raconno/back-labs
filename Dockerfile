FROM python:3.10-slim

ENV FLASK_APP=lab

COPY requirements.txt /back/

RUN python3 -m pip install -r /back/requirements.txt

COPY lab /back/lab

WORKDIR /back

CMD flask run --host 0.0.0.0 -p $PORT