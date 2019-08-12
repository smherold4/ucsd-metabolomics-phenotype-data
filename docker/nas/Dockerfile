FROM docker.elastic.co/elasticsearch/elasticsearch:6.8.1
ADD ./elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
USER root
RUN chown elasticsearch:elasticsearch config/elasticsearch.yml
ENV ELASTIC_PASSWORD=$ELASTIC_PASSWORD
USER elasticsearch
