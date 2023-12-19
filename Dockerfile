FROM leafney/docker-flask:py3
MAINTAINER Ed Brannin "edbrannin@gmail.com"
WORKDIR /app/web
RUN apk update && \
    apk add py-pillow build-base ca-certificates libffi-dev && \
    rm -rf /var/cache/apk/*
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel 

ENV FLASK_APP=contacts SIM_CONTACTS_SETTINGS=config.py FLASK_DEBUG=0

# https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#add-or-copy
# Try not to invalidate the `pip install` step by copything everything else after
COPY requirements.txt /app/web/
RUN python3 -m pip install --no-cache-dir -r requirements.txt && mkdir -p /app/web/instance

RUN rm /app/web/app.py
COPY . /app/web/
VOLUME ["/app/web/instance", "/app/web/db"]
