FROM alpine:latest

WORKDIR /app

ARG VERSION=0.8.1

RUN apk add --update curl \
    && rm -rf /var/cache/apk/*

RUN set -ex \
  && ARCH=$(arch) \
  && curl -s -L https://github.com/vcarus/volto/releases/download/v${VERSION}/volto-${VERSION}-${ARCH}-unknown-linux-musl.tar.gz | tar -zx \
  && cd volto-${VERSION}-${ARCH}-unknown-linux-musl \
  && cp volto /volto \
  && chmod +x /volto \
  && rm -rf /app

ENTRYPOINT ["/volto"]

CMD ["--config", "/etc/volto/config.toml"]
