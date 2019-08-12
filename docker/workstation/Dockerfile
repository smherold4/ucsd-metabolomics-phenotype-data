FROM docker.elastic.co/elasticsearch/elasticsearch:6.8.1
ADD ./elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
USER root
RUN chown elasticsearch:elasticsearch config/elasticsearch.yml
RUN chown -R elasticsearch:elasticsearch data
ENV ES_JAVA_OPTS="-Xms16g -Xmx16g"
RUN echo "Setting ELASTIC_PASSWORD as $ELASTIC_PASSWORD"
ENV ELASTIC_PASSWORD=$ELASTIC_PASSWORD
USER elasticsearch
