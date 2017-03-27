FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

RUN npm install -g bower grunt-cli
RUN npm install
RUN bower install
RUN grunt

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV LANG en_US.UTF-8
ENV PYTHONIOENCODING utf_8
ENV DISABLE_COLLECTSTATIC 1
