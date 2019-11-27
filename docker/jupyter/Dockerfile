FROM jupyter/scipy-notebook:17aba6048f44
ENV NB_UID=1000
ENV GRANT_SUDO=yes
ENV RESTARTABLE=yes
ADD ./pip_install_frequently_used_libraries.sh /usr/local/bin/before-notebook.d/
USER root
RUN chmod -R 777 /home/jovyan/work
