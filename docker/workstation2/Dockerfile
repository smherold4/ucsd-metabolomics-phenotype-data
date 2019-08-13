FROM docker.elastic.co/elasticsearch/elasticsearch:6.8.1
ARG ELASTIC_PASSWORD
RUN echo "Setting password as $ELASTIC_PASSWORD"
ENV ELASTIC_PASSWORD=$ELASTIC_PASSWORD

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
