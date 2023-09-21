#!/bin/bash

docker run -d --rm --name nginx -p 80:80 -v $PWD/:/etc/nginx/ nginx:1.25-alpine

