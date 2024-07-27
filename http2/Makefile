### Makefile ---

## Author: shell@mpb21
## Version: $Id: Makefile,v 0.0 2023/07/19 07:48:42 shell Exp $
## Keywords:
## X-URL:

clean:
	rm -f tls/*.pem

chown:
	sudo chown shell:shell *.pcap

stop:
	docker stop nginx

tcp_srv:
	docker run -d --rm --name nginx -p 80:80 -v $$PWD/tcp:/etc/nginx/ nginx:1.27-alpine

tcp_cli:
	curl -v --http2-prior-knowledge 'http://localhost/nginx.conf'

tcp-tcpdump:
	sudo tcpdump -i lo port 80 -w tcp.pcap

tls/key.pem:
	openssl genrsa -out $@ 1024
	chmod 644 $@

tls/cert.pem: tls/key.pem
	openssl req -new -x509 -days 3650 -key $? -out $@ -subj "/C=CN/CN=https.lan"

tls/dh.pem:
	openssl dhparam -out $@ 1024

tls_srv: tls/key.pem tls/cert.pem tls/dh.pem
	docker run -d --rm --name nginx -p 443:443 -v $$PWD/tls:/etc/nginx/ nginx:1.27-alpine

tls_cli:
	SSLKEYLOGFILE=curl_ssl_keylog curl -v -k --http2 'https://localhost/nginx.conf'

tls-tcpdump:
	sudo tcpdump -i lo port 443 -w tls.pcap

### Makefile ends here
