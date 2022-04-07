package main

import (
	"fmt"
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
	in := &pb.AddRequest{A: 10, B: 20}
	log.Printf("rpc add call, A: %d, B: %d", in.A, in.B)
	out, err := c.Add(ctx, in)
	if err != nil {
		log.Fatalf("rpc add return failed: %v", err)
	}
	log.Printf("rpc add return, N: %d", out.N)
	return
}

func proc_sum(conn *grpc.ClientConn) {
	c := pb.NewAddClient(conn)
	ctx := context.Background()

	log.Printf("rpc sum call")
	sumcli, err := c.Sum(ctx)
	if err != nil {
		log.Fatalf("rpc sum failed: %v", err)
	}

	var i int32
LOOP:
	for i = 20; i < 30; i++ {
		err = sumcli.Send(&pb.SumRequest{N: i})
		switch err {
		case nil:
		case io.EOF:
			err = nil
			break LOOP
		default:
			log.Fatalf("rpc sum stream send failed: %v", err)
		}
		log.Printf("rpc sum stream send, N: %d", i)
	}

	out, err := sumcli.CloseAndRecv()
	if err != nil {
		log.Fatalf("rpc sum return failed: %v", err)
	}
	log.Printf("rpc sum return, N: %d", out.N)
	return
}

func proc_range(conn *grpc.ClientConn) {
	c := pb.NewRangeClient(conn)
	ctx := context.Background()
	in := &pb.RangeRequest{N: 10, Len: 10}
	log.Printf("rpc range call, N: %d", in.N)
	rangecli, err := c.Range(ctx, in)
	if err != nil {
		log.Fatalf("rpc range failed: %v", err)
	}

LOOP:
	for {
		out, err := rangecli.Recv()
		switch err {
		case nil:
		case io.EOF:
			err = nil
			break LOOP
		default:
			log.Fatalf("rpc range stream recv failed: %v", err)
		}
		log.Printf("rpc range stream recv, N: %d", out.N)
	}
	return
}

func proc_echo(conn *grpc.ClientConn) {
	c := pb.NewEchoClient(conn)
	ctx := context.Background()
	waitc := make(chan interface{})

	log.Printf("rpc echo call")
	echocli, err := c.Echo(ctx)
	if err != nil {
		log.Fatalf("rpc echo failed: %v", err)
	}
	go proc_echo_recv(echocli, waitc)
	<-waitc

	var i int32
LOOP:
	for i = 10; i < 100; i += 10 {
		in := &pb.EchoRequest{N: i, S: fmt.Sprintf("%d", i)}
		err = echocli.Send(in)
		switch err {
		case nil:
		case io.EOF:
			err = nil
			break LOOP
		default:
			log.Fatalf("rpc echo stream send failed: %v", err)
		}
		log.Printf("rpc echo stream send, N: %d, S: %s", in.N, in.S)
	}
	echocli.CloseSend()
	<-waitc
	log.Printf("rpc echo end")
	return
}

func proc_echo_recv(echocli pb.Echo_EchoClient, waitc chan interface{}) {
	waitc <- nil
LOOP:
	for {
		out, err := echocli.Recv()
		switch err {
		case nil:
		case io.EOF:
			err = nil
			break LOOP
		default:
			fmt.Printf("%s", err.Error())
			log.Fatalf("rpc echo stream recv failed: %v", err)
		}
		log.Printf("rpc echo stream recv, N: %d, S: %s", out.N, out.S)
	}
	log.Printf("rpc echo stream end")
	waitc <- nil
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

	case "sum":
		proc_sum(conn)

	case "range":
		proc_range(conn)

	case "echo":
		proc_echo(conn)

	default:
		log.Fatalf("unknown command: %s", os.Args[2])

	}
	return
}
