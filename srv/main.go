package main

import (
	"io"
	"log"
	"net"
	"os"

	pb "grpctest/proto"

	"golang.org/x/net/context"
	"google.golang.org/grpc"
)

type server struct{}

func (s *server) Add(ctx context.Context, in *pb.AddRequest) (out *pb.AddResponse, err error) {
	log.Printf("rpc add in, A: %d, B: %d", in.A, in.B)
	out = &pb.AddResponse{
		N: in.A + in.B,
	}
	log.Printf("rpc add out, N: %d", out.N)
	return
}

func (s *server) Sum(stream pb.Add_SumServer) (err error) {
	log.Printf("rpc sum in")
	var n int32
	var in *pb.SumRequest

LOOP:
	for {
		in, err = stream.Recv()
		switch err {
		case nil:
		case io.EOF:
			break LOOP
		default:
			log.Fatalf("rpc sum stream recv failed: %v", err)
		}
		log.Printf("rpc sum stream recv, N: %d", in.N)
		n += in.N
	}

	err = stream.SendAndClose(&pb.SumResponse{N: n})
	if err != nil {
		log.Fatalf("rpc sum return failed: %v", err)
	}
	log.Printf("rpc sum out, N: %d", n)
	return
}

func (s *server) Range(in *pb.RangeRequest, stream pb.Range_RangeServer) (err error) {
	log.Printf("rpc range in, N: %d, len: %d", in.N, in.Len)
	for i := in.N; i < in.N+in.Len; i++ {
		err = stream.Send(&pb.RangeResponse{N: i})
		if err != nil {
			log.Fatalf("rpc range stream send failed: %v", err)
		}
		log.Printf("rpc range stream send, N: %d", i)
	}
	log.Printf("rpc range end")
	return
}

func (s *server) Echo(stream pb.Echo_EchoServer) (err error) {
	log.Printf("rpc echo in")
	var in *pb.EchoRequest
LOOP:
	for {
		in, err = stream.Recv()
		switch err {
		case nil:
		case io.EOF:
			break LOOP
		default:
			log.Fatalf("rpc echo stream recv failed: %v", err)
		}
		log.Printf("rpc echo stream recved, N: %d, S: %s", in.N, in.S)

		out := &pb.EchoResponse{N: in.N + 1, S: in.S + "echo"}
		err = stream.Send(out)
		if err != nil {
			log.Fatalf("rpc echo stream send failed: %v", err)
		}
		log.Printf("rpc echo stream sent, N: %d, S: %s", out.N, out.S)
	}
	log.Printf("rpc echo end")
	return
}

func main() {
	li, err := net.Listen("tcp", os.Args[1])
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	log.Printf("listen: %s", os.Args[1])

	s := grpc.NewServer()
	pb.RegisterAddServer(s, &server{})
	pb.RegisterRangeServer(s, &server{})
	pb.RegisterEchoServer(s, &server{})
	// Register reflection service on gRPC server.
	// reflection.Register(s)
	if err := s.Serve(li); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
	log.Printf("server stopped")
}
