FROM jupyter/scipy-notebook:17aba6048f44
ENV ELASTICSEARCH_CONFIG_URL=http://jupyter:marsearthvenusmercury4321@nas:9200
ENV GRANT_SUDO=yes
ENV RESTARTABLE=yes
ADD ./pip_install_frequently_used_libraries.sh /usr/local/bin/before-notebook.d/
USER root
RUN chmod -R 777 /home/jovyan/work
