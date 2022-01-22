#!/bin/sh

# create certificate for a domain

# verify arguments
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 domain-name"
    echo "    domain-name: the domain for which the certificate should be issued."
    exit
fi

# create private key
openssl genrsa -out "${1}.priv-key.pem" 2048

# create CSR (certificate signing request)
openssl req -new -sha256 \
    -key "${1}.priv-key.pem" \
    -subj "/C=US/ST=CA/O=Example/CN=${1}" \
    -out "${1}.csr"


# create exentions file
cat > "${1}.ext" <<EOL
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = ${1}
EOL

# create signed certificate
openssl x509 -req -in "${1}.csr" \
    -CA root-ca-certificate.crt -CAkey root-ca-private-key.pem \
    -CAcreateserial    -out "${1}.crt"    -days 825    -sha256 \
    -extfile "${1}.ext"

# set permissions
chmod 444 "${1}.crt"
chmod 400 "${1}.priv-key.pem"
chmod 400 "${1}.csr"
chmod 400 "${1}.ext"
