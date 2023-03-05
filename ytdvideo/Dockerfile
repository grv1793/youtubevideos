FROM ubuntu:18.04
MAINTAINER Gaurav Verma <gaurav.verma@workindia.in>
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
RUN apt-get update --fix-missing
RUN apt-get install -y python3.6
RUN apt-get install -y python3-pip
RUN apt-get install -y libsqlite3-dev
RUN apt-get install -y libpq-dev
RUN apt-get install -y xz-utils libxext-dev libssl-dev libxrender1 zip unzip xvfb wget libfontconfig1 libmysqlclient-dev build-essential
RUN pip3 install --upgrade pip
ADD REQUIREMENTS/development.txt /config/requirements.txt
RUN pip3 install -r /config/requirements.txt
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN python3 manage.py collectstatic --noinput
