build-srv:
	docker run --rm -v "$$PWD":/srv/ -w /srv/ gobuilder go build -o srv grpctest/srv

build-cli:
	docker run --rm -v "$$PWD":/srv/ -w /srv/ gobuilder go build -o cli grpctest/cli
