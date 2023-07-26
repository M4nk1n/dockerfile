FROM alpine:latest

ARG VERSION=tuic-server-1.0.0
ARG SYSTEM=linux-musl

WORKDIR /etc/tuic

RUN wget https://github.com/EAimTY/tuic/releases/download/${VERSION}/${VERSION}-$(uname -m)-unknown-${SYSTEM} -O /usr/bin/tuic-server \
&& chmod +x /usr/bin/tuic-server

COPY config.json /etc/tuic/

EXPOSE 443/udp

ENTRYPOINT ["tuic-server"]
CMD ["-c", "/etc/tuic/config.json"]
