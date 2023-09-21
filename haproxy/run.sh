#!/bin/bash

docker run -d --rm --name haproxy -p 80:80 -u=root -v $PWD/:/usr/local/etc/haproxy/ haproxy:2.8-alpine
