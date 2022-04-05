build-proto:
	protoc -I proto --go_out=plugins=grpc:proto proto/iface.proto

build-srv:
	docker run --rm -v "$$PWD":/srv/ -w /srv/ gobuilder go build -o bin/srv grpctest/srv
	sudo chown -R shell:shell bin/

build-cli:
	docker run --rm -v "$$PWD":/srv/ -w /srv/ gobuilder go build -o bin/cli grpctest/cli
	sudo chown -R shell:shell bin/

build-proxy:
	docker run --rm -v "$$PWD":/srv/ -w /srv/ gobuilder go build -o bin/proxy grpctest/proxy
	sudo chown -R shell:shell bin/

run-srv:
	bin/srv :50053

run-cli-add:
	bin/cli 127.0.0.1:50053 add

run-cli-range:
	bin/cli 127.0.0.1:50053 range

run-proxy:
	bin/proxy :50052 127.0.0.1:50053

tcpdump:
	sudo tcpdump -i lo -w output.pcap port 50053
	sudo chown shell:shell output.pcap

clean:
	rm -f bin/*
