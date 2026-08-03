#!/usr/bin/env bash
set -euo pipefail

sudo mkdir -p /etc/nginx/ssl

sudo openssl req \
  -x509 \
  -nodes \
  -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/shop.test.key \
  -out /etc/nginx/ssl/shop.test.crt \
  -days 365 \
  -subj "/CN=shop.test" \
  -addext "subjectAltName=DNS:shop.test"

echo "SSL certificate created for shop.test"
