.PHONY: rebuild

rebuild:
	docker-compose down --rmi all -v && \
        docker ps -a --filter name=jupyter- -q | xargs --no-run-if-empty docker rm && \
        docker network prune -f && \
        docker-compose build --no-cache && \
        docker-compose up -d
