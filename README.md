# grpc example and test

The purpose of this project is to demonstrate the usage of grpc, and test how it works.

# proto

It has four functions inside.

* Add: no stream.
* Sum: client stream.
* Range: server stream.
* Echo: bidirectional stream.

# build and run

1. To update proto stub code: `make proto/iface.pb.go`, `make proto/iface_pb2.py`
2. To download modules to vendor: `go mod vendor`
3. To build server: `make build-srv`
4. To build client: `make build-cli`
5. To run server: `make run-srv`
6. To run client: `make run-cli-add`, `make run-cli-sum`, `make run-cli-range`, `make run-cli-echo`
7. To run tcpdump: `make tcpdump`

CAUTION: The Makefile will trying to change the owner of all the generated files to `shell:shell`. That's me. Comment the lines or change the username/group to your's, if you are using golang docker image as I am.

# pcaps

Four pcap files inside, captured between golang client to golang server rpc call. To demonstrate how grpc running.

# reference

1. [gRPC使用](https://zhuanlan.zhihu.com/p/358727696)
2. [Basics tutorial](https://grpc.io/docs/languages/go/basics/#bidirectional-streaming-rpc-1)
3. [Implementing gRPC In Python: A Step-by-step Guide](https://www.velotio.com/engineering-blog/grpc-implementation-using-python)
