#!/bin/bash
# Script to generate self-signed SSL certificates for development

# Exit on error
set -e

# Create directory for certificates
mkdir -p nginx/ssl

# Generate a private key
openssl genrsa -out nginx/ssl/key.pem 2048

# Generate a certificate signing request
openssl req -new -key nginx/ssl/key.pem -out nginx/ssl/csr.pem -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Generate a self-signed certificate (valid for 365 days)
openssl x509 -req -days 365 -in nginx/ssl/csr.pem -signkey nginx/ssl/key.pem -out nginx/ssl/cert.pem

# Remove the certificate signing request (no longer needed)
rm nginx/ssl/csr.pem

echo "Self-signed SSL certificates generated successfully!"
echo "Certificate: nginx/ssl/cert.pem"
echo "Private key: nginx/ssl/key.pem"
