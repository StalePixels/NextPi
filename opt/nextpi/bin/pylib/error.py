#!/usr/bin/env python

import sys

ERR_UID_ROOT_REQUIRED = 0
ERR_INVALID_PARAMETERS = 1
ERR_MISSING_DEPENDENCY = 2
ERR_BUCKET_NOT_FOUND = 3

messages = {
	0: "Root permissions required",
	1: "Invalid Parameters",
	2: "Midding dependency",
	3: "Bucket not found"
}

def exit(code):
	sys.exit("ERROR^"+str(code)+" "+messages[code])