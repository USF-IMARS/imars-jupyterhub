FROM quay.io/jupyter/scipy-notebook:latest

# ---------------------- Your project env (unchanged) ----------------------
COPY environment.yml /tmp/environment.yml

RUN conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda env create -f /tmp/environment.yml && \
    conda clean -afy

# Make shells use your env by default (Hub still runs server from base)
ENV CONDA_DEFAULT_ENV=planetary-env
ENV PATH="/opt/conda/envs/planetary-env/bin:$PATH"

# ---------------------- Symlinks for user data ----------------------------
RUN ln -s /srv/pgs /home/jovyan/pgs && \
    ln -s /srv/yin /home/jovyan/yin

# ---------------------- ESA SNAP ------------------------------------------
RUN wget -q https://download.esa.int/step/snap/10_0/installers/esa-snap_sentinel_linux-10.0.0.sh && \
    chmod +x ./esa-snap_sentinel_linux-10.0.0.sh && \
    printf "o\n2\n/home/jovyan/esa-snap\nx,4\ny\n/usr/local/bin\nn\n" | ./esa-snap_sentinel_linux-10.0.0.sh || true && \
    rm -f ./esa-snap_sentinel_linux-10.0.0.sh

# ---------------------- MATLAB setup --------------------------------------
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxt6 libxmu6 libglu1-mesa libxrandr2 libxrender1 libxfixes3 \
    libxi6 libxcursor1 libxcomposite1 libfontconfig1 libgl1 libsm6 \
    libxext6 libx11-6 unzip && \
    rm -rf /var/lib/apt/lists/*

COPY matlab /home/jovyan/MATLAB
RUN chown -R jovyan:users /home/jovyan/MATLAB && chmod -R u+w /home/jovyan/MATLAB
USER jovyan

ENV MATLAB_ROOT=/home/jovyan/MATLAB/R2021b
ENV MLM_LICENSE_FILE=$MATLAB_ROOT/licenses/network.lic
ENV PYTHONPATH=$MATLAB_ROOT/extern/engines/python:$PYTHONPATH
ENV PATH=$MATLAB_ROOT/bin:$PATH

# 1) Install matlab_kernel into BASE Python so Hub can import it
RUN /opt/conda/bin/pip install --no-cache-dir matlab_kernel && \
    /opt/conda/bin/python -m matlab_kernel install --sys-prefix || true

# 2) Create Python 3.9 env, install MATLAB engine + matlab_kernel there,
#    and force the kernelspec under BASE prefix to use that env.
RUN mamba create -n py39-matlab -y python=3.9 && \
    conda run -n py39-matlab python -m pip install --no-cache-dir "$MATLAB_ROOT/extern/engines/python/." && \
    conda run -n py39-matlab pip install --no-cache-dir matlab_kernel && \
    conda run -n py39-matlab python -m matlab_kernel install --prefix=/opt/conda && \
    /opt/conda/bin/python -c "import json,sys; p='/opt/conda/share/jupyter/kernels/matlab/kernel.json'; \
d=json.load(open(p)); d['argv']=['/opt/conda/envs/py39-matlab/bin/python','-m','matlab_kernel','-f','{connection_file}']; \
d['display_name']='MATLAB (py39)'; open(p,'w').write(json.dumps(d))" && \
    conda clean -afy
# ==============================================================================================


# ==============================================================================================
# === Install Julia + IJulia kernel (for JupyterHub)
# ==============================================================================================
USER root
RUN apt-get update && apt-get install -y wget tar && rm -rf /var/lib/apt/lists/*

# Install Julia
ENV JULIA_VERSION=1.10.4
RUN wget https://julialang-s3.julialang.org/bin/linux/x64/${JULIA_VERSION%.*}/julia-${JULIA_VERSION}-linux-x86_64.tar.gz && \
    tar -xvzf julia-${JULIA_VERSION}-linux-x86_64.tar.gz -C /opt/ && \
    ln -s /opt/julia-${JULIA_VERSION}/bin/julia /usr/local/bin/julia && \
    rm julia-${JULIA_VERSION}-linux-x86_64.tar.gz

# Use a shared depot so IJulia (and future Julia pkgs) are installed once
ENV JULIA_DEPOT_PATH=/opt/julia-depot
RUN mkdir -p $JULIA_DEPOT_PATH && chown -R $NB_UID:$NB_GID $JULIA_DEPOT_PATH

# Install IJulia and register a kernel
USER $NB_USER
# Note: installkernel() is the correct call (install() is undefined)
RUN julia -e 'using Pkg; Pkg.add("IJulia"); using IJulia; IJulia.installkernel("Julia")'
