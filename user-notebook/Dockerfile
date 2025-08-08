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



# ==============================================================================================
# === Create symlinks for user data directories
# ==============================================================================================
# NOTE: If you edit these, you must also update jupyterhub_config.py (c.DockerSpawner.volumes)
RUN ln -s /srv/pgs /home/jovyan/pgs && \
    ln -s /srv/yin /home/jovyan/yin
# ==============================================================================================



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



# ==============================================================================================
# === MATLAB setup
# ==============================================================================================
USER root

# Copy MATLAB into the container
COPY matlab /home/jovyan/MATLAB


# Make sure permissions are correct
RUN chown -R jovyan:users /home/jovyan/MATLAB && \
    chmod -R u+w /home/jovyan/MATLAB
# === install MATLAB kernel

RUN apt-get update && apt-get install -y \
    libxt6 libxmu6 libglu1-mesa libxrandr2 libxrender1 libxfixes3 \
    libxi6 libxcursor1 libxcomposite1 libfontconfig1 \
    libgl1 libsm6 libxext6 libx11-6 unzip && \
    rm -rf /var/lib/apt/lists/*


USER jovyan

# === set environment variables
ENV MATLAB_ROOT=/home/jovyan/MATLAB/R2021b
ENV MLM_LICENSE_FILE=$MATLAB_ROOT/licenses/network.lic
ENV PYTHONPATH=$MATLAB_ROOT/extern/engines/python:$PYTHONPATH
# + matlab binary to path
ENV PATH=$MATLAB_ROOT/bin:$PATH  

# === install matlab python engine
RUN cd /home/jovyan/MATLAB/R2021b/extern/engines/python && \
    /opt/conda/envs/planetary-env/bin/python setup.py install


# === install kernel
RUN /opt/conda/envs/planetary-env/bin/pip install matlab_kernel && \
    python -m matlab_kernel install --user

# ==============================================================================================