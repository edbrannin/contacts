FROM leafney/docker-flask
MAINTAINER Ed Brannin "edbrannin@gmail.com"
WORKDIR /app/web
RUN apk update && \
    apk add py-pillow build-base python-dev && \
    rm -rf /var/cache/apk/*

ENV FLASK_APP=contacts SIM_CONTACTS_SETTINGS=config.py FLASK_DEBUG=0
CMD ["/usr/bin/python2", "-m", "flask", "run"]

COPY . /app/web
RUN pip install --no-cache-dir -r requirements.txt && mkdir -p /app/web/instance
VOLUME ["/app/web/instance", "/app/web/db"]
# ENTRYPOINT ["python"]
