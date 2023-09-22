#!/bin/bash

docker run -d --rm --name caddy -p 2019:2019 -p 80:80 -v $PWD/:/etc/caddy/ caddy:2-alpine
