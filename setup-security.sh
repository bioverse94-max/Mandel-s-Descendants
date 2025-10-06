#!/bin/bash

# Create directories for certificates
mkdir -p certs
cd certs

# Generate CA key and certificate
openssl req -x509 -nodes -newkey rsa:4096 -days 365 \
    -keyout ca.key -out ca.crt \
    -subj "/CN=BioVerse CA/O=BioVerse/C=US"

# Generate server key and CSR
openssl req -nodes -newkey rsa:2048 \
    -keyout server.key -out server.csr \
    -subj "/CN=bioverse.local/O=BioVerse/C=US"

# Sign the server certificate
openssl x509 -req -days 365 \
    -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
    -out server.crt \
    -extfile <(echo -e "subjectAltName=DNS:bioverse.local,DNS:localhost,IP:127.0.0.1")

# Generate client key and CSR
openssl req -nodes -newkey rsa:2048 \
    -keyout client.key -out client.csr \
    -subj "/CN=bioverse-client/O=BioVerse/C=US"

# Sign the client certificate
openssl x509 -req -days 365 \
    -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
    -out client.crt

# Set proper permissions
chmod 600 *.key
chmod 644 *.crt *.csr

# Create Docker secrets
if docker secret ls | grep -q "bioverse_ca_cert"; then
    docker secret rm bioverse_ca_cert
fi
docker secret create bioverse_ca_cert ca.crt

if docker secret ls | grep -q "bioverse_server_cert"; then
    docker secret rm bioverse_server_cert
fi
docker secret create bioverse_server_cert server.crt

if docker secret ls | grep -q "bioverse_server_key"; then
    docker secret rm bioverse_server_key
fi
docker secret create bioverse_server_key server.key

# Update Docker Compose configuration
cd ..
echo "Updating Docker Compose configuration..."

# Create environment file for secure configuration
cat > .env << EOL
# Security
SSL_CERT=/app/certs/server.crt
SSL_KEY=/app/certs/server.key
ELASTIC_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)
GRAFANA_PASSWORD=$(openssl rand -base64 32)

# Service configuration
WORKERS=4
MAX_REQUESTS=1000
MAX_REQUESTS_JITTER=50
PORT=8443
EOL

echo "Security setup complete! Make sure to:"
echo "1. Add the CA certificate (ca.crt) to your trusted certificates"
echo "2. Keep the .env file secure and backed up"
echo "3. Distribute client certificates as needed"