FROM python:3-alpine

WORKDIR /src

ENV PYTHONPATH "${PYTHONPATH}:/src"

RUN apk add --update \
    git \
    && rm -rf /var/cache/apk/*

ADD . /src

RUN python setup.py install
