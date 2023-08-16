FROM --platform=$BUILDPLATFORM tonistiigi/xx AS xx

FROM --platform=$BUILDPLATFORM frolvlad/alpine-glibc:latest AS build

COPY --from=xx / /

ARG VERSION=v4.0.1

RUN xx-info env && \
    ARCH=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/amd64/) && \
    wget -q -O "snell-server.zip" https://dl.nssurge.com/snell/snell-server-${VERSION}-linux-${ARCH}.zip && \
    unzip snell-server.zip && rm snell-server.zip && \
    xx-verify /snell-server

FROM frolvlad/alpine-glibc:latest

ENV TZ=UTC

COPY --from=build /snell-server /usr/bin/snell-server

RUN apk add --update --no-cache libstdc++

ENTRYPOINT ["/usr/bin/snell-server","-c","/config/snell-server.conf"]