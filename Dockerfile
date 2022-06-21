from python:3.8

RUN mkdir /opt/website2
COPY . /opt/website2
WORKDIR /opt/website2

RUN pip install pipenv; pipenv sync

CMD pipenv run gunicorn -c /opt/website2/gunicorn.conf.py server:app

