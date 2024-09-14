### Makefile --- 

## Author: shell@dsk
## Version: $Id: Makefile,v 0.0 2024/09/14 11:24:12 shell Exp $
## Keywords: 
## X-URL: 

run:
	docker run -d --name msqt -p 1883:1883 -p 9001:9001 -v $$PWD/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto

sub:
	docker exec -it msqt mosquitto_sub -h localhost -t test/#

pub:
	docker exec -it msqt mosquitto_pub -h localhost -t test -m 'test'
	docker exec -it msqt mosquitto_pub -h localhost -t test1 -m 'test1'
	docker exec -it msqt mosquitto_pub -h localhost -t test/deep -m 'test/deep'
	docker exec -it msqt mosquitto_pub -h localhost -t test/deep/more -m 'test/deep/more'

### Makefile ends here
