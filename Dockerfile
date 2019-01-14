FROM python:2.7

RUN apt-get update && \
        apt-get install -y gfortran

RUN pip install numpy yt

WORKDIR /usr/src/

COPY . /usr/src/
