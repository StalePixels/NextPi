#!/bin/sh

# Enter the source tree
cd src

# Bootstrap the (originally SVN) envrionment
./tools/svn-bootstrap.sh

# Configure the build chain, let it know we don't use /usr/local
./configure --prefix=/usr

# Now build
make