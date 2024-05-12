FROM python:3.11-slim-buster

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install wheel setuptools

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN touch /app/backend.log

COPY . /app

EXPOSE 8080
