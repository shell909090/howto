test:
	docker run -d --name traefik -p 8080:8080 -p 80:80 -v $$PWD:/etc/traefik/ -v /var/run/docker.sock:/var/run/docker.sock traefik:3.0
