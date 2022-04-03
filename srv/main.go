package main

import (
	"log"
	"net"

	pb "grpctest/proto"

	"golang.org/x/net/context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

const (
	addr = ":50051"
)

type server struct{}

func (s *server) Add(ctx context.Context, in *pb.AddRequest) (out *pb.AddResponse, err error) {
	log.Printf("A: %d, B: %d", in.A, in.B)
	out = &pb.AddResponse{
		N: in.A + in.B,
	}
	return
}

func main() {
	li, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	s := grpc.NewServer()
	pb.RegisterAddServer(s, &server{})
	// Register reflection service on gRPC server.
	reflection.Register(s)
	if err := s.Serve(li); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
