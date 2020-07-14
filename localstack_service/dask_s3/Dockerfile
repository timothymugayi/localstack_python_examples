FROM jupyter/base-notebook:lab

USER root

RUN apt-get update \
    && apt-get install -yq --no-install-recommends graphviz git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_USER

RUN conda install --yes \
    -c conda-forge \
    python-blosc=1.7.0 \
    cytoolz \
    dask==2.17.2 \
    lz4==2.2.1 \
    nomkl \
    dask-ml==1.5.0 \
    distributed==2.17.0 \
    numpy==1.18.4 \
    pandas==1.0.3 \
    s3fs==0.4.2 \
    ipywidgets \
    dask-labextension==2.0.2 \
    python-graphviz \
    && jupyter labextension install @jupyter-widgets/jupyterlab-manager dask-labextension@2.0.2 \
    && conda clean -tipsy \
    && jupyter lab clean \
    && jlpm cache clean \
    && npm cache clean --force \
    && find /opt/conda/ -type f,l -name '*.a' -delete \
    && find /opt/conda/ -type f,l -name '*.pyc' -delete \
    && find /opt/conda/ -type f,l -name '*.js.map' -delete \
    && find /opt/conda/lib/python*/site-packages/bokeh/server/static -type f,l -name '*.js' -not -name '*.min.js' -delete \
    && rm -rf /opt/conda/pkgs

USER root

# Create the /opt/app directory, and assert that Jupyter's NB_UID/NB_GID values
# haven't changed.
RUN mkdir /opt/app \
    && if [ "$NB_UID" != "1000" ] || [ "$NB_GID" != "100" ]; then \
    echo "Jupyter's NB_UID/NB_GID changed, need to update the Dockerfile"; \
    exit 1; \
    fi

COPY prepare.sh /usr/bin/prepare.sh

USER $NB_USER

ENTRYPOINT ["tini", "--", "/usr/bin/prepare.sh"]
CMD ["start.sh", "jupyter", "lab"]
