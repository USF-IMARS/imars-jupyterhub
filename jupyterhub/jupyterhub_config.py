c = get_config()

from dockerspawner import DockerSpawner

# Use DockerSpawner to launch user notebooks in containers
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = 'imars-scipy-notebook'
c.Spawner.default_url = '/lab'

# Admin users
c.Authenticator.admin_users = {'tylar'}
# Optional: Disallow PAM to open sessions directly
c.PAMAuthenticator.open_sessions = False

# Networking configuration
c.JupyterHub.hub_ip = 'jupyterhub'  # Service name in docker-compose
c.JupyterHub.hub_connect_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8081
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = 'imars-jupyterhub_default'



# Allow the Lab UI’s origin to connect via WS
c.JupyterHub.allow_origin = '*'           # or more restrictively 'http://manglillo.marine.usf.edu:8000'
c.JupyterHub.allow_origin_pat = '.*'
c.NotebookApp.disable_check_xsrf = True    # only if you’re OK with that risk

# Environment variables for MATLAB in user containers
c.DockerSpawner.environment = {
    'MATLAB_ROOT': '/home/jovyan/MATLAB/R2021b',
    'MLM_LICENSE_FILE': '/home/jovyan/MATLAB/R2021b/licenses/license.dat'
}

# data volumes for users
# NOTE: if you edit these you must edit the symlinks in
#       user-notebook/Dockerfile too
c.DockerSpawner.volumes = {
    'tpa_pgs': '/srv/pgs',
    'yin': '/srv/yin',
}

# allow long timeouts
c.MappingKernelManager.kernel_startup_timeout = 120
c.MappingKernelManager.kernel_info_timeout    = 120


c.DockerSpawner.cmd = ["jupyter", "lab",
    "--NotebookApp.allow_origin='*'",
    "--NotebookApp.disable_check_xsrf=True",
    "--ip=0.0.0.0",
    "--no-browser",
]
