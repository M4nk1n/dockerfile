FROM nginx

COPY version /tmp/ariang-version

RUN set -eu; \
  version="$(cat /tmp/ariang-version)"; \
  printf '%s\n' "$version" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$'; \
  apt-get update; \
  apt-get install -y --no-install-recommends ca-certificates curl unzip; \
  curl -fsSL --retry 3 \
    "https://github.com/mayswind/AriaNg/releases/download/${version}/AriaNg-${version}.zip" \
    -o /tmp/ariang.zip; \
  unzip -oq /tmp/ariang.zip -d /usr/share/nginx/html; \
  rm -f /tmp/ariang.zip /tmp/ariang-version; \
  apt-get purge -y --auto-remove curl unzip; \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]
