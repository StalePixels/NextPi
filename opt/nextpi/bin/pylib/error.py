#!/usr/bin/env python

import sys

ERR_UID_ROOT_REQUIRED = 1
ERR_INVALID_PARAMETERS = 2
ERR_MISSING_DEPENDENCY = 3
ERR_BUCKET_NOT_FOUND = 4
ERR_FILE_NOT_FOUND = 5

messages = {
	1: "Root permissions required",
	2: "Invalid Parameters",
	3: "Missing dependency",
	4: "Bucket not found",
	5: "File not found"
}

def exit(code):
	sys.stderr.write("ERROR^"+str(code)+" "+messages[code])
	sys.exit(code)