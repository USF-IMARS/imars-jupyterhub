.PHONY: rebuild

NETWORK=imars-jupyterhub_default

rebuild:
	@echo "✔️ Stopping and removing Compose-managed containers and volumes..."
	docker-compose down --rmi all -v

	@echo "✔️ Removing stale containers using imars-scipy-notebook..."
	-docker ps -a --filter ancestor=imars-scipy-notebook -q | xargs --no-run-if-empty docker rm -f
	docker-compose down --rmi all -v

	@echo "pruning volumes..."
	-docker volume prune -f

	@echo "✔️ Ensuring Docker network '$(NETWORK)' exists..."
	-docker network inspect $(NETWORK) >/dev/null 2>&1 || docker network create $(NETWORK)

	@echo "✔️ Ensuring Docker volumes for NFS mounts exist..."
	-docker volume inspect tpa_pgs >/dev/null 2>&1 || docker volume create --driver local --opt type=nfs4 --opt o=rw,addr=131.247.188.131 --opt device=:/data/tylarmurray tpa_pgs
	-docker volume inspect yin >/dev/null 2>&1 || docker volume create --driver local --opt type=nfs4 --opt o=rw,addr=192.168.1.203 --opt device=:/yin/homes yin

	@echo "✔️ Rebuilding images without cache..."
	docker-compose build --no-cache

	@echo "✔️ Starting containers..."
	docker-compose up -d

	@echo "✔️ Rebuild complete. Verify with: docker-compose ps"
