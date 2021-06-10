#!/bin/sh

# Ensure we have everything we need
sudo apt-get install build-essential -y

# This package is so simple we don't even use ./configure, but if it did, use /usr
echo "We don't need no stinking.... ./configure --prefix=/usr"

# Now build
make

