# Use Ubuntu as the base image
FROM       ubuntu:latest
MAINTAINER A. Rachez <arnaud.rachez@gmail.com>

# Install recsys dependencies
RUN apt-get update
RUN apt-get install -y python-dev
RUN apt-get install -y python-scipy python-numpy
RUN apt-get install -y python-pip
RUN pip install csc-pysparse networkx divisi2

# Install recsys
RUN apt-get install -y git
RUN git clone https://github.com/ocelma/python-recsys.git recsys
RUN cd recsys && python setup.py install

# Launch script
COPY recommender /recommender
WORKDIR /recommender

CMD ["python", "recommender.py"]