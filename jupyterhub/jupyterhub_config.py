c = get_config()

from dockerspawner import DockerSpawner

# Spawner / image
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = 'imars-scipy-notebook'

# Land on JupyterLab (without breaking the Hub base_url)
c.Spawner.default_url = '/lab'

# Admins / auth
c.Authenticator.admin_users = {'tylar'}
c.PAMAuthenticator.open_sessions = False

# Networking
c.JupyterHub.hub_ip = 'jupyterhub'      # service name from docker-compose
c.JupyterHub.hub_connect_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8081
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = 'imars-jupyterhub_default'

# CORS (optional; keep as tight as you can)
c.JupyterHub.allow_origin = '*'
c.JupyterHub.allow_origin_pat = '.*'
# DO NOT disable XSRF on the user server; Hub handles auth/cookies securely.
# If you must, prefer ServerApp flags inside the image, not here.

# Env in user containers
c.DockerSpawner.environment = {
    'MATLAB_ROOT': '/home/jovyan/MATLAB/R2021b',
    'MLM_LICENSE_FILE': '/home/jovyan/MATLAB/R2021b/licenses/license.dat',
}

# Volumes
c.DockerSpawner.volumes = {
    'tpa_pgs': '/srv/pgs',
    'yin': '/srv/yin',
}

# Timeouts
c.MappingKernelManager.kernel_startup_timeout = 120
c.MappingKernelManager.kernel_info_timeout    = 120

# ⛔️ REMOVE the plain "jupyter lab" command — it breaks the base_url.
# c.DockerSpawner.cmd = ["jupyter", "lab", ...]  # <-- DELETE THIS

# ✅ Use the JupyterHub-aware single-user entrypoint instead:
# If your image is based on Jupyter Docker Stacks, this script exists:
c.DockerSpawner.cmd = ["start-singleuser.sh"]

# Fallback if your image doesn't have start-singleuser.sh:
# c.DockerSpawner.cmd = ["jupyterhub-singleuser"]
