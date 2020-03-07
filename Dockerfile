FROM python:3.8-alpine

# Hotfix for glibc hack that fixes the order of DNS resolving (i.e. check /etc/hosts first and then lookup DNS-servers).
# To fix this we just create /etc/nsswitch.conf and add the following line:
ONBUILD RUN echo 'hosts: files mdns4_minimal [NOTFOUND=return] dns mdns4' >> /etc/nsswitch.conf

COPY ./requirements.txt /tmp/requirements.txt

RUN apk add --update postgresql-dev gcc python3-dev musl-dev && \
    rm /var/cache/apk/* && \
    pip install --upgrade pip && pip install setuptools --upgrade && \
    pip install -r /tmp/requirements.txt

# for static files
RUN mkdir -p /var/www/ac-rank/static/

ADD . /ac_rank
RUN chmod +x /ac_rank/docker-entrypoint.sh

WORKDIR /ac_rank

ENTRYPOINT ["/ac_rank/docker-entrypoint.sh"]
