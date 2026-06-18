This is the setup for a jupyterHub server for IMaRS at USF CMS.
Currently being run on manglillo.

Users can log in with ssh username & password.

## Prerequisites

Before running docker-compose, the following external volumes must be created on the hypervisor:

### tpa_pgs (NFS)
```bash
docker volume create \
  --driver local \
  --opt type=nfs4 \
  --opt o=rw,addr=131.247.188.131 \
  --opt device=:/data/tylarmurray \
  tpa_pgs
```

### yin (NFS)
```bash
docker volume create \
  --driver local \
  --opt type=nfs4 \
  --opt o=rw,addr=192.168.1.203 \
  --opt device=:/yin/homes \
  yin
```

### thing2 (CIFS/SMB)
```bash
docker volume create \
  --driver local \
  --opt type=cifs \
  --opt o=username=imars,password=PASSWORD_GOES_HERE \
  --opt device=//thing2.marine.usf.edu/Shared \
  thing2
```

Replace `<PASSWORD>` with the actual password for the imars account.

These volumes are defined as external in docker-compose.yml and must exist before the services can start.

## HTTPS

HTTPS is handled by an nginx reverse proxy with Let's Encrypt certificates, following the same pattern as [mbon-dashboard-server](https://github.com/marinebon/mbon-dashboard-server).

### Initial certificate setup

Before starting nginx for the first time, obtain certificates (requires port 80 to be free; run as root):

```bash
./cert_update.sh
```

This stops nginx, runs certbot in standalone mode, copies `fullchain.pem` and `privkey.pem` into `./certs/`, and starts nginx.

### Automatic renewal

Add a root cron job on the host, for example:

```text
0 0,12 * * * cd /path/to/imars-jupyterhub && /bin/bash ./cert_update.sh
```

### Access

JupyterHub is served at `https://manglillo.marine.usf.edu/` (ports 80 and 443). The hub container is no longer published directly on port 8000.

If using OAuth, set the callback URL to `https://manglillo.marine.usf.edu/hub/oauth_callback`.

### Troubleshooting 502 Bad Gateway

nginx returns 502 when it cannot reach JupyterHub on port 8000. On the host:

```bash
docker compose ps
docker logs jupyterhub --tail 100
docker exec nginx wget -qO- http://jupyterhub:8000/hub/health
```

If `jupyterhub` is restarting or unhealthy, fix the hub first (missing NFS volumes, Docker socket permissions, etc.). After changing nginx config, rebuild and restart:

```bash
docker compose up --build -d nginx
```


