#!/usr/bin/env python

import os, sys
from . import pienv, error

def root_check():
	if not pienv.DEVMODE:
		if os.geteuid() != 0:
			error.exit(error.ERR_UID_ROOT_REQUIRED)
			
def exit(message = None):
	
	if message:
		sys.stdout.write("OK^"+message)
		sys.exit(0)
	else:
		sys.stdout.write("OK")
		sys.exit(0)
