FROM jupyter/scipy-notebook:17aba6048f44
ARG JUPYTER_PASSWORD
ENV ELASTICSEARCH_CONFIG_URL=http://jupyter:${JUPYTER_PASSWORD}@nas:9200
ENV GRANT_SUDO=yes
ENV RESTARTABLE=yes
ADD ./pip_install_frequently_used_libraries.sh /usr/local/bin/before-notebook.d/
USER root
RUN chmod -R 777 /home/jovyan/work
CMD start-notebook.sh --NotebookApp.token=${JUPYTER_PASSWORD}
