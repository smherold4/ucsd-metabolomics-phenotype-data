FROM docker.elastic.co/elasticsearch/elasticsearch:7.3.1
ARG ELASTIC_PASSWORD
ENV ELASTIC_PASSWORD=$ELASTIC_PASSWORD

ARG AWS_ACCESS_KEY
ARG AWS_SECRET_KEY

ADD ./elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
ADD ./jvm.options /usr/share/elasticsearch/config/jvm.options

RUN mkdir -p /usr/share/elasticsearch/config/certificates
ADD ./ca.crt /usr/share/elasticsearch/config/certificates/ca.crt
ADD ./es.crt /usr/share/elasticsearch/config/certificates/es.crt
ADD ./es.key /usr/share/elasticsearch/config/certificates/es.key

USER root
RUN chown elasticsearch:elasticsearch config/elasticsearch.yml
RUN chown -R elasticsearch:elasticsearch data
USER elasticsearch
RUN bin/elasticsearch-plugin install -b repository-s3
RUN bin/elasticsearch-keystore create
RUN echo $AWS_ACCESS_KEY | bin/elasticsearch-keystore add --stdin s3.client.default.access_key
RUN echo $AWS_SECRET_KEY | bin/elasticsearch-keystore add --stdin s3.client.default.secret_key
