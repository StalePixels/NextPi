#!/usr/bin/env python
import os

DEVMODE = False
READWRITE = False

if os.path.isfile("/tmp/nextpi.dev"):
    DEVMODE = True
    READWRITE = True
