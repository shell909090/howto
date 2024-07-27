# http2 over tcp

* 启动服务: `make tcp_srv`
* 停止服务: `make stop`
* 客户端访问: `make tcp_cli`
* tcpdump: `make tcp_tcpdump`

# http2 over tls

* 启动服务: `make tls_srv`
* 停止服务: `make stop`
* 客户端访问: `make tls_cli`
* tcpdump: `make tls_tcpdump`

使用wireshark分析的时候，记得设定SSLKEYLOGFILE。详见下参考“tls,http2,grpc的拦截分析”。

# 参考

* [Hypertext Transfer Protocol Version 2 (HTTP/2)](https://datatracker.ietf.org/doc/html/rfc7540)
* [HTTP2规范](https://hanpfei.github.io/2016/10/29/http2-spec/)
* [HTTP/2 and How it Works](https://cabulous.medium.com/http-2-and-how-it-works-9f645458e4b2)
* [tls,http2,grpc的拦截分析](https://blog.shell909090.org/blog/archives/2884/)
* [HTTP/2 Frame Types](https://webconcepts.info/concepts/http2-frame-type/)
