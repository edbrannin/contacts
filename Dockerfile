FROM ubuntu:latest
MAINTAINER Ed Brannin "edbrannin@gmail.com"
RUN apt-get update -y \
 && apt-get install -y \
            python-pip \
            python-dev \
            build-essential \
 && rm -rf /var/lib/apt/lists/*
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt && mkdir -p /app/instance
ENV FLASK_APP=contacts SIM_CONTACTS_SETTINGS=config.py FLASK_DEBUG=0
VOLUME ["/app/instance", "/app/db"]
# ENTRYPOINT ["python"]
CMD ["/usr/bin/python2", "-m", "flask", "run"]
