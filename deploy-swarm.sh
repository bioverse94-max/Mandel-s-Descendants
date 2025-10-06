#!/bin/bash

# Initialize Swarm mode if not already in swarm mode
if ! docker info | grep -q "Swarm: active"; then
    echo "Initializing Docker Swarm mode..."
    docker swarm init
fi

# Build images
echo "Building Docker images..."
docker build -t bioverse-backend:latest ./backend
docker build -t bioverse-scibert:latest ./scibert-master

# Deploy the stack
echo "Deploying the stack..."
docker stack deploy -c docker-stack.yml bioverse

# Wait for services to start
echo "Waiting for services to start..."
sleep 10

# Check service status
echo "Checking service status..."
docker service ls

# Set up auto-scaling rules
echo "Setting up auto-scaling rules..."
docker service update --replicas 2 bioverse_backend
docker service update --replicas 2 bioverse_scibert

echo "Setup complete! Monitor the services with:"
echo "docker service ls"
echo "docker service logs bioverse_backend"
echo "docker service logs bioverse_scibert"