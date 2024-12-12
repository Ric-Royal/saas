#!/bin/bash

# Create SSL directory
mkdir -p /etc/nginx/ssl

# Generate strong DH parameters (4096 bits)
openssl dhparam -out /etc/nginx/ssl/dhparam.pem 4096

# Generate private key with stronger parameters
openssl genrsa -out /etc/nginx/ssl/privkey.pem 4096

# Generate CSR with modern parameters
openssl req -new -sha256 \
    -key /etc/nginx/ssl/privkey.pem \
    -out /etc/nginx/ssl/server.csr \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Generate self-signed certificate
openssl x509 -req -sha256 -days 365 \
    -in /etc/nginx/ssl/server.csr \
    -signkey /etc/nginx/ssl/privkey.pem \
    -out /etc/nginx/ssl/fullchain.pem \
    -extensions v3_ca \
    -extfile <(echo "[v3_ca]
basicConstraints = critical, CA:FALSE
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = DNS:localhost, DNS:*.localhost")

# Create chain.pem for OCSP stapling
cp /etc/nginx/ssl/fullchain.pem /etc/nginx/ssl/chain.pem

# Set proper permissions
chmod 600 /etc/nginx/ssl/privkey.pem
chmod 600 /etc/nginx/ssl/server.csr
chmod 600 /etc/nginx/ssl/dhparam.pem
chmod 644 /etc/nginx/ssl/fullchain.pem
chmod 644 /etc/nginx/ssl/chain.pem

echo "SSL certificates and DH parameters generated successfully"
echo "Note: For production, replace self-signed certificates with Let's Encrypt or other trusted CA certificates"
echo "Warning: The DH parameter generation may take several minutes due to the increased key size" 