FROM python:3.10.8-alpine3.16

RUN adduser -D nsu

WORKDIR /home/nsu
COPY . .
RUN chmod +x boot.sh
#COPY requirements.txt requirements.txt
RUN \
     apk add --no-cache postgresql-libs && \
     apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
     python -m venv venv && \
     venv/bin/pip install -r requirements.txt

ENV FLASK_APP nsu.py

RUN chown -R nsu:nsu ./
USER nsu
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]