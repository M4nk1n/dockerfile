FROM alpine:latest

ARG SYSTEM=linux-musl

WORKDIR /etc/tuic
COPY version /tmp/version

RUN VERSION="tuic-server-$(cat /tmp/version)" && wget https://github.com/EAimTY/tuic/releases/download/${VERSION}/${VERSION}-$(uname -m)-unknown-${SYSTEM} -O /usr/bin/tuic-server \
&& chmod +x /usr/bin/tuic-server

COPY config.json /etc/tuic/

EXPOSE 443/udp

ENTRYPOINT ["tuic-server"]
CMD ["-c", "/etc/tuic/config.json"]
