#!/bin/bash

# Enter the source tree
cd src

#Nothing grand, but allows the CI to wrap this operation to build custom packages for NextPi
sudo cp build/csid /usr/bin
sudo cp build/csidl /usr/bin