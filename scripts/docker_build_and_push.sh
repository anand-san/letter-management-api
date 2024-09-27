#!/bin/bash

# Check if a tag name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <tag-name>"
  exit 1
fi

# Assign the tag name to a variable
TAG_NAME=$1

# Hardcoded prefix for the Docker image name
IMAGE_PREFIX="anandsandilya/letters-management-api"

# Full image name with tag
FULL_IMAGE_NAME="$IMAGE_PREFIX:$TAG_NAME"

# Build the Docker image
docker build -t $FULL_IMAGE_NAME .

# Check if the build was successful
if [ $? -ne 0 ]; then
  echo "Docker build failed"
  exit 1
fi

# Push the Docker image to Docker Hub
docker push $FULL_IMAGE_NAME

# Check if the push was successful
if [ $? -ne 0 ]; then
  echo "Docker push failed"
  exit 1
fi

echo "Docker image $FULL_IMAGE_NAME built and pushed successfully"