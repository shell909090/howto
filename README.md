# how to

Quick tour to how to use something.

# OCR

* [tesseract](tesseract)

# ASR

* [faster-whisper](faster-whisper)
* [whisper](whisper)
* [sensevoice](sensevoice)

# db

* [redis](redis)

# queue

* [rabbitmq](rabbitmq)
* [mosquitto](mosquitto)

# stream lib

* [grpc](grpc)
* [websocket](websocket)

# reverse proxy

* [traefik](traefik)
* [envoy](envoy)
* [haproxy](haproxy)
* [nginx](nginx)
* [caddy](caddy)

traefik和各种系统的集成最佳（docker/k8s/etc）。envoy适合api重编程流量路径，和mesh绝配。haproxy性能最高，但内存消耗较大，且http模式下各种复杂功能受限。nginx功能强大资源消耗小，且是唯一对301的response location重写的proxy。caddy配置看似简单实际上掌握和调试困难。

# protocol

* [http2](http2)

# performance

* [profile-flame](prof-flame)
* [profile-memory](prof-mem)

# ebpf

* [bcc](ebpf/bcc.md)
