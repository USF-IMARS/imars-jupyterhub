FROM quay.io/jupyter/scipy-notebook:latest

COPY environment.yml /tmp/environment.yml

# Install conda env
RUN conda env create -f /tmp/environment.yml && \
    conda clean -afy

# Optional: activate environment by default
RUN echo "conda activate planetary-env" >> ~/.bashrc

# Activate environment in the notebook server
ENV CONDA_DEFAULT_ENV=planetary-env
ENV PATH="/opt/conda/envs/planetary-env/bin:$PATH"

# create symlinks for user data directories
# NOTE: if you edit these you must edit juptyer/jupyterhub_config.py c.DockerSpawner.volumes too
RUN ln -s /srv/pgs /home/jovyan/pgs && \
    ln -s /srv/yin /home/jovyan/yin

# ==============================================================================================
# === install ESA SNAP
# ==============================================================================================
RUN wget https://download.esa.int/step/snap/10_0/installers/esa-snap_sentinel_linux-10.0.0.sh && \
    chmod +x ./esa-snap_sentinel_linux-10.0.0.sh && \
    printf "o\n2\n/opt/esa-snap\nx,4\ny\n/usr/local/bin\nn\n" | ./esa-snap_sentinel_linux-10.0.0.sh
# ==============================================================================================
