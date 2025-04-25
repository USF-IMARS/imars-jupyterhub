# setup of environment based on docs
# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/recipes.html#using-mamba-install-recommended-or-pip-install-in-a-child-docker-image

ARG BASE_IMAGE=quay.io/jupyter/base-notebook
FROM $BASE_IMAGE

RUN mamba install --yes 'flake8' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Install from the requirements.txt file
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/
RUN mamba install --yes --file /tmp/requirements.txt && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"



## Install in the default python3 environment
#RUN pip install --no-cache-dir 'flake8' && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"
#
## Install from the requirements.txt file
#COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/
#RUN pip install --no-cache-dir --requirement /tmp/requirements.txt && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"