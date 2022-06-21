# website2

This repository is an overhaul of https://github.com/ksnavely/website. It's on Python 3.8 due to nosetests.
The project is docker-forward, includes gunicorn, and is targeted for usage in Kubernetes.

## Dev setup

Local dev:
```
python setup.py install
make test
```

## Docker running / dev:
```
make build-image
make run-docker-gunicorn

curl 127.0.0.1:5000/version
  {"ok":true,"version":"0.1.0"}
```

