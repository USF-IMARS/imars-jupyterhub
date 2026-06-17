This is the setup for a jupyterHub server for IMaRS at USF CMS.
Currently being run on manglillo.

Users sign in via OAuth2/OIDC (configured in `.env`). See [OAuth setup](#oauth-setup) below.

## OAuth setup

1. Register an OAuth2/OIDC application with your identity provider (Google Workspace, GitHub, Keycloak, university SSO, etc.).
2. Set the redirect URI to:
   ```
   https://<your-jupyterhub-host>:8000/hub/oauth_callback
   ```
3. Copy the example env file and fill in your provider details:
   ```bash
   cp .env.example .env
   ```
4. Set `OAUTH_ALLOWED_USERS` to a comma-separated list of usernames (as returned by your provider's `OAUTH_USERNAME_CLAIM`). Every user who should access the hub must be listed here unless you set `OAUTH_ALLOW_ALL=true` for testing.
5. Rebuild and restart:
   ```bash
   docker-compose build jupyterhub
   docker-compose up -d
   ```

### Example: GitHub

In `.env`:

```
OAUTH_CALLBACK_URL=https://manglillo.example.edu:8000/hub/oauth_callback
OAUTH_CLIENT_ID=<github-app-client-id>
OAUTH_CLIENT_SECRET=<github-app-client-secret>
OAUTH_AUTHORIZE_URL=https://github.com/login/oauth/authorize
OAUTH_TOKEN_URL=https://github.com/login/oauth/access_token
OAUTH_USERDATA_URL=https://api.github.com/user
OAUTH_LOGIN_SERVICE=GitHub
OAUTH_USERNAME_CLAIM=login
OAUTH_SCOPE=read:user
OAUTH_ALLOWED_USERS=tylar,newuser
OAUTH_ADMIN_USERS=tylar
```

### Example: Google (OIDC)

```
OAUTH_CALLBACK_URL=https://manglillo.example.edu:8000/hub/oauth_callback
OAUTH_CLIENT_ID=<google-client-id>.apps.googleusercontent.com
OAUTH_CLIENT_SECRET=<google-client-secret>
OAUTH_AUTHORIZE_URL=https://accounts.google.com/o/oauth2/v2/auth
OAUTH_TOKEN_URL=https://oauth2.googleapis.com/token
OAUTH_USERDATA_URL=https://openidconnect.googleapis.com/v1/userinfo
OAUTH_LOGIN_SERVICE=Google
OAUTH_USERNAME_CLAIM=email
OAUTH_SCOPE=openid email profile
OAUTH_ALLOWED_USERS=you@gmail.com,colleague@gmail.com
```

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


