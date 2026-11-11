FROM alpine:latest

WORKDIR /app
COPY version /tmp/version

RUN apk add --update curl \
    && rm -rf /var/cache/apk/*

RUN set -ex \
  && VERSION=$(cat /tmp/version) \
  && ARCH=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/amd64/) \
  && curl -s -L https://github.com/fatedier/frp/releases/download/v${VERSION}/frp_${VERSION}_linux_${ARCH}.tar.gz | tar -zx \
  && cd frp_${VERSION}_linux_${ARCH} \
  && cp frps /frps \
  && cp frpc /frpc \
  && chmod +x /frps \
  && chmod +x /frpc \
  && rm -rf /app

ENTRYPOINT ["/frps","-c","/config/frps.toml"]
