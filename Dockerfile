FROM python:buster

WORKDIR /usr/src/cyclones_scraper

COPY tasks/requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY tasks ./tasks
COPY scraper ./scraper
COPY repo ./repo

WORKDIR tasks

CMD ["celery"]

