package main

import (
	"io"
	"log"
	"net"
	"os"
)

type Proxy struct {
	li          net.Listener
	listen_addr string
	target_addr string
}

func NewProxy(listen_addr, target_addr string) (p *Proxy, err error) {
	li, err := net.Listen("tcp", listen_addr)
	if err != nil {
		return
	}
	log.Printf("listen: %s", listen_addr)
	return &Proxy{
		li:          li,
		listen_addr: listen_addr,
		target_addr: target_addr,
	}, nil
}

func (p *Proxy) Close() (err error) {
	return p.li.Close()
}

func (p *Proxy) AcceptLoop() (err error) {
	for {
		conn, err := p.li.Accept()
		if err != nil {
			log.Fatalf("failed to accept: %v", err)
		}
		go p.HandleConn(conn)
	}
}

func (p *Proxy) HandleConn(src net.Conn) {
	defer src.Close()

	dst, err := net.Dial("tcp", p.target_addr)
	if err != nil {
		log.Fatalf("failed to connect: %s, %v", p.target_addr, err)
	}
	log.Printf("connect to: %s", p.target_addr)

	go io.Copy(src, dst)
	io.Copy(dst, src)
}

func main() {
	p, err := NewProxy(os.Args[1], os.Args[2])
	if err != nil {
		log.Fatalf("failed to create proxy: %v", err)
	}
	defer p.Close()

	p.AcceptLoop()
}
