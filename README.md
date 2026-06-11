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


