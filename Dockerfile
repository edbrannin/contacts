FROM python:2
MAINTAINER Ed Brannin "edbrannin@gmail.com"
# RUN apt-get update -y
# RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt && mkdir -p /app/instance
ENV FLASK_APP=contacts SIM_CONTACTS_SETTINGS=config.py FLASK_DEBUG=0
VOLUME ["/app/instance", "/app/db"]
# ENTRYPOINT ["python"]
CMD ["/usr/bin/python2 -m flask run"]
