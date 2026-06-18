#!/bin/bash
# NOTE: This works along with a cronjob similar to the following in order to update ssl certs automatically.
# This cronjob must be run as root.
# example crontab entry:
# 0 0,12 * * * cd /path/to/imars-jupyterhub && /bin/bash ./cert_update.sh
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

DOMAIN=manglillo.marine.usf.edu
CERTS_DIR="$(pwd)/certs"

docker stop nginx 2>/dev/null || true

docker run --rm \
  -v "$CERTS_DIR:/etc/letsencrypt" \
  -v "$CERTS_DIR:/var/lib/letsencrypt" \
  -p 80:80 \
  certbot/certbot certonly \
  --standalone \
  -d "$DOMAIN" \
  --email tylarmurray@usf.edu \
  --agree-tos \
  --no-eff-email \
  --non-interactive

cp "$CERTS_DIR/live/$DOMAIN/"*.pem "$CERTS_DIR"/.

docker compose up --build -d nginx
