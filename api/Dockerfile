FROM python:buster

WORKDIR /usr/src/cyclones_api

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY cyclones_api.py .
COPY models.py .

ENV FLASK_APP=cyclones_api.py

