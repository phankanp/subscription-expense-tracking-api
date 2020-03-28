# pull base image
FROM python:3.7.5-alpine

# set environment variables
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# create and set work directory 
RUN mkdir /app 
WORKDIR /app
COPY ./app /app

# create a user for running application
RUN adduser -D user
USER user

