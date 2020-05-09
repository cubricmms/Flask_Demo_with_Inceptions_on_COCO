FROM python:3.7-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev 
RUN apk add zlib libjpeg-turbo-dev libpng-dev freetype-dev lcms2-dev libwebp-dev harfbuzz-dev fribidi-dev tcl-dev tk-dev
RUN apk add --no-cache gcc musl-dev linux-headers

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV FLASK_DEBUG 1
ENV SECRET_KEY "SECRET_HERE"
ENV FLASK_ENV development
ENV FLASK_APP run.py
ENV FLASK_RUN_HOST 0.0.0.0

ENV DATABASE_URL postgresql://jing:test@db:5432/flask
ENV SQLALCHEMY_TRACK_MODIFICATIONS = False


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/

