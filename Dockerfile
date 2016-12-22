FROM python:3.5
MAINTAINER James Maddox
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN mkdir /src
WORKDIR /src
ADD requirements.txt .
RUN pip install -r requirements.txt --src /usr/local/src
ADD . .
CMD [".docker/run.sh"]
