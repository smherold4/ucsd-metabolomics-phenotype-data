FROM docker.elastic.co/elasticsearch/elasticsearch:6.8.1
ADD ./elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
USER root
RUN chown elasticsearch:elasticsearch config/elasticsearch.yml
RUN chown -R elasticsearch:elasticsearch data
ENV ES_JAVA_OPTS="-Xms4g -Xmx4g"
USER elasticsearch
