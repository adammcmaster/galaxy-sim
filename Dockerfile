FROM python:2.7

RUN apt-get update && \
        apt-get install -y gfortran

WORKDIR /usr/src/

COPY requirements.txt /usr/src/

RUN pip install -r requirements.txt

COPY amr2cube.f90 /usr/src/

RUN f2py -c amr2cube.f90 -m amr2cube

RUN mv /usr/src/amr2cube.so /usr/local/lib/python2.7/

COPY . /usr/src/
