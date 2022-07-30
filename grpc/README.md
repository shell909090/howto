# grpc example and test

The purpose of this project is to demonstrate the usage of grpc, and test how it works.

# proto

It has four functions inside.

* Add: no stream.
* Sum: client stream.
* Range: server stream.
* Echo: bidirectional stream.

# requirement

* protoc: [Protocol Buffer Compiler Installation](https://grpc.io/docs/protoc-installation/)
* Go plugins: [Quick start](https://grpc.io/docs/languages/go/quickstart/)
* Python Plugins: [Quick start](https://grpc.io/docs/languages/python/quickstart/)
  * `pip3 install grpcio grpcio-tools`

# build and run

1. To update proto stub code: `make proto/iface.pb.go`, `make proto/iface_pb2.py`
2. To download modules to vendor: `go mod vendor`
3. To build go server: `make build-srv`
4. To build go client: `make build-cli`
5. To run server: `make run-srv`, `make run-pysrv`
6. To run go client: `make run-cli-add`, `make run-cli-sum`, `make run-cli-range`, `make run-cli-echo`
7. To run python client: `make run-pycli-add`, `make run-pycli-sum`, `make run-pycli-range`, `make run-pycli-echo`
8. To run tcpdump: `make tcpdump`
9. To clean up: `make clean`

CAUTION: The Makefile will trying to change the owner of all the generated files to `shell:shell`. That's me. Comment the lines or change the username/group to your's, if you are using golang docker image as I am.

# pcaps

Four pcap files inside, captured between golang client to golang server rpc call. To demonstrate how grpc running.

# reference

1. [gRPC使用](https://zhuanlan.zhihu.com/p/358727696)
2. [Basics tutorial](https://grpc.io/docs/languages/go/basics/#bidirectional-streaming-rpc-1)
3. [Implementing gRPC In Python: A Step-by-step Guide](https://www.velotio.com/engineering-blog/grpc-implementation-using-python)
