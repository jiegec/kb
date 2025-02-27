# DNS over HTTPS (DoH)

标准：[RFC 8484](https://datatracker.ietf.org/doc/html/rfc8484)

请求格式：

1. DNS 格式 GET 版，把 DNS 的请求进行 base64url 编码作为 dns 参数传入，并设置 `accept: application/dns-message`：

	```
	:method = GET
	:scheme = https
	:authority = dnsserver.example.net
	:path = /dns-query?dns=AAABAAABAAAAAAAAA3d3dwdleGFtcGxlA2NvbQAAAQAB
	accept = application/dns-message
	```

2. DNS 格式 POST 版，把 DNS 的请求作为 Payload 传入，设置 `accept: application/dns-message` 和 `content-type: application/dns-message`：

	```
	:method = POST
	:scheme = https
	:authority = dnsserver.example.net
	:path = /dns-query
	accept = application/dns-message
	content-type = application/dns-message
	content-length = 33

	<33 bytes represented by the following hex encoding>
	00 00 01 00 00 01 00 00  00 00 00 00 03 77 77 77
	07 65 78 61 6d 70 6c 65  03 63 6f 6d 00 00 01 00
	01
	```

3. 此外部分 DoH 服务器还支持 RFC 8484 以外的 [JSON 格式](https://developers.google.com/speed/public-dns/docs/doh/json)：

	```
	:method = GET
	:scheme = https
	:authority = dnsserver.example.net
	:path = /dns-query?name=baidu.com&type=A
	accept = application/dns-json
	```

测试方法：

- RFC 8484: `curl -H 'accept: application/dns-message' 'https://SERVER/dns-query?dns=q80BAAABAAAAAAAAA3d3dwdleGFtcGxlA2NvbQAAAQAB' | hexdump -c`
- JSON API: `curl -H 'accept: application/dns-json' 'https://SERVER/dns-query?name=baidu.com&type=A'`

公开的 DoH 服务：

- [Google Public DNS](https://developers.google.com/speed/public-dns/docs/doh):
	- https://dns.google/dns-query – RFC 8484 (GET and POST)
	- https://dns.google/resolve? – JSON API (GET)
	- 实测两个 endpoint 都支持 RFC 8484 和 JSON API
- [Cloudflare 1.1.1.1](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/):
	- https://cloudflare-dns.com/dns-query - RFC 8484 and JSON API
- [DNSPod](https://www.dnspod.cn/products/publicdns):
	- https://doh.pub/dns-query - RFC 8484 and JSON API
- [Alibaba Cloud Public DNS](https://www.alibabacloud.com/help/en/dns/what-is-alibaba-cloud-public-dns)
	- https://223.5.5.5/dns-query - RFC 8484，不支持 JSON API
