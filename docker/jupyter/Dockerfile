FROM jupyter/scipy-notebook:17aba6048f44
ENV ELASTICSEARCH_CONFIG_URL=http://jupyter:marsearthvenusmercury4321@nas:9200
ENV GRANT_SUDO=yes
ENV RESTARTABLE=yes
ADD ./startup.sh /usr/local/bin/before-notebook.d/
USER root
RUN chown -R jovyan:jovyan /usr/local/bin/before-notebook.d/
USER jovyan
