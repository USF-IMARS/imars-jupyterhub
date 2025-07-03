c = get_config()

from dockerspawner import DockerSpawner

c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = 'quay.io/jupyter/scipy-notebook'
c.Spawner.default_url = '/lab'

c.Authenticator.admin_users = {'tylar'}
# optional: allow any valid system user
c.PAMAuthenticator.open_sessions = False


# Configure networking so user containers can reach the Hub
c.JupyterHub.hub_ip = 'jupyterhub'  # use the service name from docker-compose
c.JupyterHub.hub_port = 8081

c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = 'imars-jupyterhub_default'

