# pull base image
FROM python:3.7.5-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
  && apk add build-base jpeg-dev zlib-dev postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# create and set work directory 
RUN mkdir /app 
WORKDIR /app

# copy entrypoint.sh
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# copy project
COPY ./app /app

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]