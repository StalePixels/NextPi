#!/bin/sh

# Enter the source tree
cd src

# This package is so simple we don't even use ./configure, but if it did, use /usr
echo "We don't need no stinking.... ./configure --prefix=/usr"

# Now build
make