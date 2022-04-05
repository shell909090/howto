package main

import (
	"io"
	"log"
	"os"

	pb "grpctest/proto"

	"golang.org/x/net/context"
	"google.golang.org/grpc"
)

func proc_add(conn *grpc.ClientConn) {
	c := pb.NewAddClient(conn)
	ctx := context.Background()
	req := &pb.AddRequest{A: 10, B: 20}
	log.Printf("rpc call add: A: %d, B: %d", req.A, req.B)
	resp, err := c.Add(ctx, req)
	if err != nil {
		log.Fatalf("could not get result: %v", err)
	}
	log.Printf("rpc add return, N: %d", resp.N)
	return
}

func proc_range(conn *grpc.ClientConn) {
	c := pb.NewRangeClient(conn)
	ctx := context.Background()
	req := &pb.RangeRequest{N: 10}
	log.Printf("rpc call range: N: %d", req.N)
	resp, err := c.Range(ctx, req)
	if err != nil {
		log.Fatalf("could not get result: %v", err)
	}

	for {
		recv, err := resp.Recv()
		switch err {
		case nil:
		case io.EOF:
			return
		default:
			log.Fatalf("could not get stream: %v", err)
		}
		log.Printf("rpc range stream, N: %d", recv.N)
	}
	return
}

func main() {
	log.Printf("connnect to: %s", os.Args[1])

	conn, err := grpc.Dial(os.Args[1], grpc.WithInsecure())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	log.Printf("connected to the target")

	switch os.Args[2] {
	case "add":
		proc_add(conn)

	case "range":
		proc_range(conn)

	default:
		log.Fatalf("unknown command: %s", os.Args[2])

	}
	return
}
