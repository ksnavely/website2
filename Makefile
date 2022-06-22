build-image:
	docker build -t kdevops-website:testing .

run-docker:
	docker run -p 127.0.0.1:5000:5000 kdevops-website:testing

run-docker-gunicorn:
	docker run -p 127.0.0.1:5000:5000 kdevops-website:testing pipenv run gunicorn -c /opt/website2/gunicorn.conf.py server:app

run-docker-bash:
	docker run -it -p 127.0.0.1:5000:5000 kdevops-website:testing /bin/bash

run-local-flask:
	FLASK_APP=website/server flask run

run-local-gunicorn:
	pipenv run gunicorn -c /opt/website2/gunicorn.conf.py server:app

test:
	pipenv run nosetests -s tests

black:
	pipenv run black website/ tests/

push-testing:
	docker tag kdevops-website:testing ksnavely/website:testing; docker push ksnavely/website:testing
