FROM alpine:latest

WORKDIR /app

ARG VERSION=0.51.2

RUN apk add --update curl \
    && rm -rf /var/cache/apk/*

RUN set -ex \
  && ARCH=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/amd64/) \
  && curl -s -L frp_${VERSION}_linux_${ARCH}.tar.gz https://github.com/fatedier/frp/releases/download/v${VERSION}/frp_${VERSION}_linux_${ARCH}.tar.gz | tar -zx \
  && cd frp_${VERSION}_linux_${ARCH} \
  && cp frps /frps \
  && cp frpc /frpc \
  && chmod +x /frps \
  && chmod +x /frpc \
  && rm -rf /app

ENTRYPOINT ["/frps","-c","/config/frps.ini"]
