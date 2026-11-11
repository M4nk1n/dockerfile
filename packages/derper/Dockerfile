FROM --platform=$BUILDPLATFORM alpine:3.22 AS builder

RUN apk add --no-cache ca-certificates curl tar
WORKDIR /src
COPY version /tmp/version
RUN VERSION=$(cat /tmp/version) \
    && printf '%s\n' "$VERSION" | grep -Eq '^v[0-9]+\.[0-9]+\.[0-9]+$' \
    && curl --retry 3 -fL "https://codeload.github.com/tailscale/tailscale/tar.gz/refs/tags/${VERSION}" -o /tmp/source.tar.gz \
    && tar -xzf /tmp/source.tar.gz --strip-components=1 \
    && rm /tmp/source.tar.gz

# Follow the release's own toolchain, which can precede the official Go images.
RUN REV=$(cat go.toolchain.rev) \
    && printf '%s\n' "$REV" | grep -Eq '^[0-9a-f]{40}$' \
    && case "$(apk --print-arch)" in x86_64) ARCH=amd64 ;; aarch64) ARCH=arm64 ;; *) exit 1 ;; esac \
    && curl --retry 3 -fL "https://github.com/tailscale/go/releases/download/build-${REV}/linux-${ARCH}.tar.gz" -o /tmp/go.tar.gz \
    && mkdir -p /usr/local/go \
    && tar -C /usr/local/go --strip-components=1 -xzf /tmp/go.tar.gz \
    && rm /tmp/go.tar.gz

ENV PATH=/usr/local/go/bin:$PATH
ARG TARGETARCH
RUN VERSION=$(cat /tmp/version) \
    && CGO_ENABLED=0 GOOS=linux GOARCH=$TARGETARCH go build -trimpath \
       -ldflags="-s -w -X tailscale.com/version.longStamp=${VERSION#v} -X tailscale.com/version.shortStamp=${VERSION#v}" \
       -o /out/derper ./cmd/derper

FROM alpine:3.22
RUN apk add --no-cache ca-certificates && mkdir -p /var/lib/derper
COPY --from=builder /out/derper /usr/local/bin/derper
EXPOSE 80/tcp 443/tcp 3478/udp
ENTRYPOINT ["/usr/local/bin/derper"]
CMD ["-c", "/var/lib/derper/derper.key", "-certdir", "/var/lib/derper/certs"]
