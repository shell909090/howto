### Makefile --- 

## Author: shell@dsk
## Version: $Id: Makefile,v 0.0 2023/08/16 14:51:59 shell Exp $
## Keywords: 
## X-URL: 
TAG=7-alpine
FLAGS=-d --restart=always

clean:
	sudo chown -R shell:shell .
	rm -f */redis.log */dump.rdb */nodes.conf

single:
	docker run ${FLAGS} --name redis -p 6379:6379 redis:${TAG}

master-slave:
	docker run ${FLAGS} --name master -p 6379:6379 -v $$PWD/master/:/data/ redis:${TAG} redis-server redis.conf
	docker run ${FLAGS} --name slave -p 6378:6379 -v $$PWD/slave/:/data/ redis:${TAG} redis-server redis.conf

stop-master-slave:
	docker stop master
	docker rm master
	docker stop slave
	docker rm slave

sentinel:
	docker run ${FLAGS} --name redis1 --net=host -v $$PWD/redis1/:/data/ redis:${TAG} redis-server redis.conf
	docker run ${FLAGS} --name redis2 --net=host -v $$PWD/redis2/:/data/ redis:${TAG} redis-server redis.conf
	docker run ${FLAGS} --name redis3 --net=host -v $$PWD/redis3/:/data/ redis:${TAG} redis-server redis.conf
	sleep 1
	docker run ${FLAGS} --name sentinel1 --net=host -v $$PWD/sentinel1/:/data/ redis:${TAG} redis-server sentinel.conf --sentinel
	docker run ${FLAGS} --name sentinel2 --net=host -v $$PWD/sentinel2/:/data/ redis:${TAG} redis-server sentinel.conf --sentinel
	docker run ${FLAGS} --name sentinel3 --net=host -v $$PWD/sentinel3/:/data/ redis:${TAG} redis-server sentinel.conf --sentinel

stop-sentinel:
	docker stop sentinel1
	docker stop sentinel2
	docker stop sentinel3
	docker rm sentinel1
	docker rm sentinel2
	docker rm sentinel3
	docker stop redis1
	docker stop redis2
	docker stop redis3
	docker rm redis1
	docker rm redis2
	docker rm redis3

cluster:
	docker run ${FLAGS} --name cluster1 --net=host -v $$PWD/cluster1/:/data/ redis:${TAG} redis-server redis.conf
	docker run ${FLAGS} --name cluster2 --net=host -v $$PWD/cluster2/:/data/ redis:${TAG} redis-server redis.conf
	docker run ${FLAGS} --name cluster3 --net=host -v $$PWD/cluster3/:/data/ redis:${TAG} redis-server redis.conf
	sleep 1
	docker run -it --rm redis:7-alpine redis-cli --cluster create 192.168.33.51:6377 192.168.33.51:6379 192.168.33.51:6378

stop-cluster:
	docker stop cluster1
	docker stop cluster2
	docker stop cluster3
	docker rm cluster1
	docker rm cluster2
	docker rm cluster3

### Makefile ends here
