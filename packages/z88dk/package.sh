#!/bin/bash

# Enter the source tree
cd src

#Nothing grand, but allows the CI to wrap this operation to build custom packages for NextPi
sudo cp -rv 1.99C 2.0 2.1 2.2pre /opt/nextpi/z88dk/


VERSION="20210721"
NAME="z88dk"

PACKAGE_NAME="$NAME-$VERSION-`cat ../../opt/nextpi/VERSION`"

echo $PACKAGE_NAME
