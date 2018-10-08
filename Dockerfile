FROM ubuntu:18.04
LABEL maintainer="xzfantom"

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
 && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN pip install Flask

RUN mkdir /opt/app
WORKDIR /opt/app

# RUN git clone https://github.com/xzfantom/bankparser.git .
ADD . .
RUN python3 setup.py install

EXPOSE 5000
ENTRYPOINT ["manage.py"]
