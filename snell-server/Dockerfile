FROM bitnami/minideb:latest

WORKDIR /app

ARG SYSTEM=linux
ARG VERSION=v4.0.1

RUN apt update && apt install -y wget unzip \
  && ARCH=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/amd64/) \
  && wget -O snell-server-${VERSION}-${SYSTEM}-${ARCH}.zip https://dl.nssurge.com/snell/snell-server-${VERSION}-${SYSTEM}-${ARCH}.zip \
  && unzip snell-server-${VERSION}-${SYSTEM}-${ARCH}.zip \
  && cp snell-server /snell-server \
  && chmod +x /snell-server \
  && apt clean \
  && rm -rf /app

ENTRYPOINT ["/snell-server","-c","/config/snell-server.conf"]
