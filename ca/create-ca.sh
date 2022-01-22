#!/bin/sh

# create Root CA's private key
# > enter a strong password when prompted
openssl genrsa -des3 -out root-ca-private-key.pem 2048

# create and self sign CA's root certificate
openssl req -x509 -new -nodes -key root-ca-private-key.pem -sha256 -days 1825 -out root-ca-certificate.crt

# Sample Information (feel free to use the default values)
# Country Name (2 letter code) [AU]:US
# State or Province Name (full name) [Some-State]:California
# Locality Name (eg, city) []:San-Francisco
# Organization Name (eg, company) [Example]:
# Organizational Unit Name (eg, section) [Technical Unit]:
# Common Name (e.g. server FQDN or YOUR name) []:example.com
# Email Address []:admin@example.com

# Change the permissions on the files
# > allow read access to owner only
chmod 400 root-ca-private-key.pem
# > allow read access to (public) certificate by everyone
chmod 444 root-ca-certificate.crt
