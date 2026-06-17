c = get_config()

import os

from dockerspawner import DockerSpawner


def _env(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and not value:
        raise ValueError(f"Required environment variable {name} is not set")
    return value


def _env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_set(name, default=None):
    raw = os.environ.get(name, "")
    if not raw:
        return set(default or [])
    return {item.strip() for item in raw.split(",") if item.strip()}


# Spawner / image
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = 'imars-scipy-notebook'

# Land on JupyterLab (without breaking the Hub base_url)
c.Spawner.default_url = '/lab'

# OAuth (GenericOAuthenticator — works with OIDC and other OAuth2 providers)
c.JupyterHub.authenticator_class = 'generic-oauth'

c.GenericOAuthenticator.client_id = _env('OAUTH_CLIENT_ID', required=True)
c.GenericOAuthenticator.client_secret = _env('OAUTH_CLIENT_SECRET', required=True)
c.GenericOAuthenticator.oauth_callback_url = _env('OAUTH_CALLBACK_URL', required=True)
c.GenericOAuthenticator.authorize_url = _env('OAUTH_AUTHORIZE_URL', required=True)
c.GenericOAuthenticator.token_url = _env('OAUTH_TOKEN_URL', required=True)
c.GenericOAuthenticator.userdata_url = _env('OAUTH_USERDATA_URL', required=True)
c.GenericOAuthenticator.login_service = _env('OAUTH_LOGIN_SERVICE', 'Sign in')

scope = _env('OAUTH_SCOPE', 'openid email profile')
c.GenericOAuthenticator.scope = scope.split()
c.GenericOAuthenticator.username_claim = _env('OAUTH_USERNAME_CLAIM', 'preferred_username')

# Authorization: OAuthenticator denies everyone by default.
allowed_users = _env_set('OAUTH_ALLOWED_USERS')
if allowed_users:
    c.OAuthenticator.allowed_users = allowed_users
elif _env_bool('OAUTH_ALLOW_ALL'):
    c.OAuthenticator.allow_all = True
else:
    raise ValueError(
        "Set OAUTH_ALLOWED_USERS (comma-separated) or OAUTH_ALLOW_ALL=true"
    )

admin_users = _env_set('OAUTH_ADMIN_USERS', default=['tylar'])
if admin_users:
    c.Authenticator.admin_users = admin_users

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

# Use the JupyterHub-aware single-user entrypoint instead:
c.DockerSpawner.cmd = ["start-singleuser.sh"]
