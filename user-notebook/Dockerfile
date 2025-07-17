FROM quay.io/jupyter/scipy-notebook:latest

COPY environment.yml /tmp/environment.yml

# Set up conda-forge and install environment
RUN conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda env create -f /tmp/environment.yml && \
    conda clean -afy

# Optional: activate environment by default
RUN echo "conda activate planetary-env" >> ~/.bashrc

# Activate environment in the notebook server
ENV CONDA_DEFAULT_ENV=planetary-env
ENV PATH="/opt/conda/envs/planetary-env/bin:$PATH"

# Create symlinks for user data directories
# NOTE: If you edit these, you must also update jupyterhub_config.py (c.DockerSpawner.volumes)
RUN ln -s /srv/pgs /home/jovyan/pgs && \
    ln -s /srv/yin /home/jovyan/yin

# ==============================================================================================
# === Install ESA SNAP
# ==============================================================================================
# NOTE: This will **always** return success.
#       The installer could fail silently.
#       This is done because the installer returns 1 even when it is successful.
RUN wget https://download.esa.int/step/snap/10_0/installers/esa-snap_sentinel_linux-10.0.0.sh && \
    chmod +x ./esa-snap_sentinel_linux-10.0.0.sh && \
    printf "o\n2\n/home/jovyan/esa-snap\nx,4\ny\n/usr/local/bin\nn\n" | ./esa-snap_sentinel_linux-10.0.0.sh || true
# ==============================================================================================
