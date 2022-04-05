package main

import (
	"log"
	"net"
	"os"

	pb "grpctest/proto"

	"golang.org/x/net/context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
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

func (s *server) Range(in *pb.RangeRequest, stream pb.Range_RangeServer) (err error) {
	log.Printf("rpc range in, N: %d", in.N)
	for i := in.N; i < in.N+10; i++ {
		err = stream.Send(&pb.RangeResponse{N: i})
		if err != nil {
			log.Printf("stream send failed: %d", i)
			return
		}
		log.Printf("rpc range out, N: %d", i)
	}
	log.Printf("rpc range end")
	return
}

// rpc ListFeatures(Rectangle) returns (stream Feature) {}
// func (s *routeGuideServer) ListFeatures(rect *pb.Rectangle, stream pb.RouteGuide_ListFeaturesServer) error {

func main() {
	li, err := net.Listen("tcp", os.Args[1])
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	log.Printf("listen: %s", os.Args[1])

	s := grpc.NewServer()
	pb.RegisterAddServer(s, &server{})
	pb.RegisterRangeServer(s, &server{})
	// Register reflection service on gRPC server.
	reflection.Register(s)
	if err := s.Serve(li); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
	log.Printf("server stopped")
}
