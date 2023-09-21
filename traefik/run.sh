#!/bin/bash

docker run -d --name traefik -p 80:80 -p 8080:8080 -v $PWD/:/etc/traefik/ -v /var/run/docker.sock:/var/run/docker.sock traefik:3.0
