package main

import (
	"log"

	pb "grpctest/proto"

	"golang.org/x/net/context"
	"google.golang.org/grpc"
)

const (
	addr = "localhost:50051"
)

func main() {
	// Set up a connection to the server.
	conn, err := grpc.Dial(addr, grpc.WithInsecure())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewAddClient(conn)

	ctx := context.Background()
	req := &pb.AddRequest{A: 10, B: 20}
	resp, err := c.Add(ctx, req)
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}
	log.Printf("N: %d", resp.N)
}
