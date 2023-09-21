#!/bin/bash

docker run -d --rm --name envoy -p 80:80 -p 9901:9901 -v $PWD/:/etc/envoy/ envoyproxy/envoy:v1.27-latest
