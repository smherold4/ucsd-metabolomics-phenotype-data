FROM docker.elastic.co/elasticsearch/elasticsearch:6.8.1
ADD ./docker-config/nas-config.yml /usr/share/elasticsearch/config/elasticsearch.yml
USER root
RUN chown elasticsearch:elasticsearch config/elasticsearch.yml
USER elasticsearch
