FROM python:2.7

RUN apt-get update && \
        apt-get install -y gfortran

WORKDIR /usr/src/

COPY requirements.txt /usr/src/

RUN pip install -r requirements.txt

COPY . /usr/src/
