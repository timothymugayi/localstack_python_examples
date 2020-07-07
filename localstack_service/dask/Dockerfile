FROM continuumio/miniconda3:4.7.12

LABEL maintainer="Timothy Mugayi <timothy.mugayi@kinesso.com>"

ENV CONDA_VERSION 4.8.3
RUN conda update conda && conda install conda=$CONDA_VERSION
RUN mkdir /opt/app /etc/dask
COPY prepare.sh /usr/bin/prepare.sh
ADD environment.yml /opt/app/

RUN /opt/conda/bin/conda env update -f /opt/app/environment.yml \
    && conda clean -tipsy \
    && find /opt/conda/ -type f,l -name '*.a' -delete \
    && find /opt/conda/ -type f,l -name '*.pyc' -delete \
    && find /opt/conda/ -type f,l -name '*.js.map' -delete \
    && find /opt/conda/lib/python*/site-packages/bokeh/server/static -type f,l -name '*.js' -not -name '*.min.js' -delete \
    && rm -rf /opt/conda/pkgs

RUN chmod +x /usr/bin/prepare.sh
COPY dask.yaml /etc/dask/
ENTRYPOINT ["tini", "-g", "--", "/usr/bin/prepare.sh"]