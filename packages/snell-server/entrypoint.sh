#!/bin/ash

set -e

BIN="/usr/bin/snell-server"
CONF="/etc/snell-server.conf"

# reuse existing config when the container restarts

run_bin() {
  echo "Running snell-server with config:"
  cat ${CONF}
  echo ""
  ${BIN} -c ${CONF}
}

if [ -f ${CONF} ]; then
  echo "Found existing config..."
  run_bin
else
  if [ -z ${PSK} ]; then
    PSK=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 16)
    echo "Using generated PSK: ${PSK}"
  else
    echo "Using predefined PSK: ${PSK}"
  fi

  echo "Generating new config..."
  echo "[snell-server]" >>${CONF}
  echo "listen = :::${PORT:-6160}" >> ${CONF}
  echo "psk = ${PSK}" >> ${CONF}
  echo "ipv6 = ${IPV6:-false}" >> ${CONF}

  # DNS
  if [ ${DNS} ]; then
    echo "dns = ${DNS}" >> ${CONF}
  fi

  # obfs
  if [ ${OBFS} ]; then
    echo "obfs = ${OBFS}" >> ${CONF}
  fi

  # obfs-host
  if [ ${OBFS_HOST} ]; then
    echo "obfs-host = ${OBFS_HOST}" >> ${CONF}
  fi

  echo "Done."
  echo ""

  run_bin
fi
