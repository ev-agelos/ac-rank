FROM python:3.8-slim-buster

# for static files
RUN mkdir -p /var/www/ac-rank/static/

RUN apt-get update && apt-get install -y --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

ADD . /ac_rank
RUN chmod +x /ac_rank/docker-entrypoint.sh

WORKDIR /ac_rank

ENTRYPOINT ["/ac_rank/docker-entrypoint.sh"]
