#!/bin/bash

# Build Docker Image
echo ">>>>>> Building Docker Image <<<<<<<"
make build

# CHeck if docker build is successful
if [ $? -ne 0 ]; then
  echo ">>>>>> Building Docker Image Failed <<<<<<<"
  exit 1
fi

# Install helm chart
echo ">>>>>> Installing HELM Chart <<<<<<<"
make install

# CHeck if Helm chart installation is successful
if [ $? -ne 0 ]; then
  echo ">>>>>> Failed to Install Helm Chart <<<<<<<"
  exit 1
fi

echo "Successfully Deployed Elevator :)"
