FROM python:3.7.0-alpine3.8
LABEL maintainer="xzfantom"

RUN pip install Flask

RUN mkdir /opt/app
WORKDIR /opt/app

ADD . .

EXPOSE 5000
ENTRYPOINT ["python3", "src/manage.py"]
