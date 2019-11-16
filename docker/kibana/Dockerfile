FROM docker.elastic.co/kibana/kibana:7.3.1
ARG ELASTIC_PASSWORD
ADD ./kibana.yml /usr/share/kibana/config/kibana.yml
USER root
RUN sed -i -e "s/{password}/${ELASTIC_PASSWORD}/g" config/kibana.yml
RUN chown kibana:kibana config/kibana.yml
USER kibana
