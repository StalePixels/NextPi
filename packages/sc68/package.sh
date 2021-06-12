#!/bin/bash

# Enter the source tree
cd src

#Nothing grand, but allows the CI to wrap this operation to build custom packages for NextPi
sudo cp -rv usr /


VERSION="3.0.0.692"
NAME="sc68"

PACKAGE_NAME="$NAME-$VERSION-`cat ../../opt/nextpi/VERSION`"

echo $PACKAGE_NAME