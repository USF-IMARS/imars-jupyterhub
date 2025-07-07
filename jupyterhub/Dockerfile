FROM jupyterhub/jupyterhub:4.0

RUN pip install dockerspawner

# === Install conda packages
# Install Miniconda
ENV CONDA_DIR=/opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
RUN apt-get update && apt-get install -y curl bzip2 && \
    curl -sLo ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash ~/miniconda.sh -b -p $CONDA_DIR && \
    rm ~/miniconda.sh && \
    $CONDA_DIR/bin/conda clean -afy

# Add your conda environment (optional)
COPY environment.yml environment.yml
RUN conda env update -n base -f environment.yml