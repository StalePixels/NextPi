#!/usr/bin/env python

import os, hashlib, shutil
from . import utils, pienv, error

PCACHE = "/PCache"
DATADIR = PCACHE+"/DATA/"
CATALOGDIR = PCACHE+"/CATALOG/"
BUCKETDB = "bucket.lst"
TMPDIR = "/tmp/"


# Make Persistence Cache readonly.
def write_enable():
	if not pienv.READWRITE:
		utils.root_check()
		os.system('/bin/mount '+PCACHE+' -o remount,rw');


# Make Persistence Cache writable.
def write_disable():
	if not pienv.READWRITE:
		utils.root_check()
		os.system('/bin/mount '+PCACHE+' -o remount,ro');


# Initalise an empty cache, presumes no cache already exists in PCACHE location.
def initalise():
	if os.path.isdir(PCACHE):
		print PCACHE+" exists"
		write_enable()
		print "Creating cache data directory: "+DATADIR
		if os.path.exists(DATADIR):
			write_disable()
			error.exit(error.ERR_UNEXPECTED_STATE)
		os.mkdir(DATADIR)
		print "Creating cache catalog directory: "+CATALOGDIR
		if os.path.exists(CATALOGDIR):
			write_disable()
			error.exit(error.ERR_UNEXPECTED_STATE)
		os.mkdir(CATALOGDIR)
		print "Creating empty bucketlist: "+CATALOGDIR+BUCKETDB
		if os.path.exists(CATALOGDIR+BUCKETDB):
			write_disable()
			error.exit(error.ERR_UNEXPECTED_STATE)
		open(CATALOGDIR+BUCKETDB, 'a').close()
		write_disable()
		exit()
	error.exit(error.ERR_MISSING_DEPENDENCY)


# Initalise an empty cache, presumes no cache already exists in PCACHE location.
def remove():
	if os.path.isdir(PCACHE):
		print PCACHE+" exists"
		write_enable()
		print "Removing cache data directory: "+DATADIR
		if not os.path.exists(DATADIR):
			write_disable()
			error.exit(error.ERR_UNEXPECTED_STATE)
		shutil.rmtree(DATADIR)
		print "Creating cache catalog directory: "+CATALOGDIR
		if not os.path.exists(CATALOGDIR):
			write_disable()
			error.exit(error.ERR_UNEXPECTED_STATE)
		shutil.rmtree(CATALOGDIR)
		write_disable()
		exit()
	error.exit(error.ERR_MISSING_DEPENDENCY)

# Compute bucketname from readable name.
#   Is currently MD5 sum based, may change at later date to reduce clashes.
def bucket_getnamehash(name):
	return hashlib.md5(name).hexdigest()

# Get complete path to bucket on currently active cache
#   Returns absolute path string
def bucket_getpath(buckethash):
	return DATADIR+buckethash
	
# Create a new bucket.
#	Does not error if already exists.
#	Does not touch bucket if already exists.
def bucket_create(buckethash, comment):
	utils.root_check()
	newDB = open(TMPDIR+BUCKETDB,"w")
	if os.path.isfile(CATALOGDIR+BUCKETDB):
		bucketDB = open(CATALOGDIR+BUCKETDB,"r")
		for bucketDBentry in bucketDB:
			bucketEntry = bucketDBentry.split(":")
			if bucketEntry[0] != buckethash:
				newDB.write(bucketDBentry)
		bucketDB.close()
		
	newDB.write(buckethash + ":" + comment + "\n")
	
	newDB.close()
	
	write_enable()
	bucket_path = bucket_getpath(buckethash)
	if not os.path.isdir(bucket_path):
		os.mkdir(bucket_path)
	shutil.move(TMPDIR+BUCKETDB, CATALOGDIR+BUCKETDB)
	write_disable()	


# Touch (aka mark as most recently used) bucket.
#	Generates a ERR_MISSING_DEPENDENCY if DB not found
#	Generates a ERR_BUCKET_NOT_FOUND if Bucket not found
#	Returns True if bucket found, and touched
def bucket_touch(buckethash):
	utils.root_check()
	thisBucket = None
	if os.path.isfile(CATALOGDIR+BUCKETDB):
		bucketDB = open(CATALOGDIR+BUCKETDB,"r")
		newDB = open(TMPDIR+BUCKETDB,"w")
		for bucketDBentry in bucketDB:
			bucketEntry = bucketDBentry.split(":")
			if bucketEntry[0] != buckethash:
				newDB.write(bucketDBentry)
			else:
				thisBucket = bucketDBentry
		bucketDB.close()
	else:
		error.exit(error.ERR_MISSING_DEPENDENCY)
		
	if thisBucket is None:
		newDB.close()
		os.remove(TMPDIR+BUCKETDB)
		error.exit(error.ERR_BUCKET_NOT_FOUND)
	else:
		newDB.write(thisBucket)
		newDB.close()
	
	write_enable()
	shutil.move(TMPDIR+BUCKETDB, CATALOGDIR+BUCKETDB)
	write_disable()
	return True


# Check if a bucket exists.
#	Returns True if found.
#	Returns False if not found
#	Generates a ERR_MISSING_DEPENDENCY if DB not found
def bucket_find(buckethash):
	if os.path.isfile(CATALOGDIR+BUCKETDB):
		bucketDB = open(CATALOGDIR+BUCKETDB,"r")
		for bucketDBentry in bucketDB:
			bucketEntry = bucketDBentry.split(":")
			if bucketEntry[0] == buckethash:
				bucketDB.close()
				return True
		return False
	else:
		error.exit(error.ERR_MISSING_DEPENDENCY)


# Delete a bucket and its contents.
#	Returns buckethash if found.
#	Returns False if not found
#	Generates a ERR_MISSING_DEPENDENCY if DB not found
def bucket_delete(buckethash):
	utils.root_check()
	thisBucket = None
	if os.path.isfile(CATALOGDIR+BUCKETDB):
		bucketDB = open(CATALOGDIR+BUCKETDB,"r")
		newDB = open(TMPDIR+BUCKETDB,"w")
		for bucketDBentry in bucketDB:
			bucketEntry = bucketDBentry.split(":")
			if bucketEntry[0] != buckethash:
				newDB.write(bucketDBentry)
			else:
				thisBucket = bucketEntry
		bucketDB.close()
		newDB.close()
	else:
		error.exit(error.ERR_MISSING_DEPENDENCY)
	
	if thisBucket is None:
		os.remove(TMPDIR+BUCKETDB)
		return False
	
	write_enable()
	shutil.rmtree(bucket_getpath(thisBucket[0]))
	shutil.move(TMPDIR+BUCKETDB, CATALOGDIR+BUCKETDB)
	write_disable()
	return thisBucket[0]


# Recursively check the size of a bucket.
#	Returns size in bytes if found.
#	Generates an error otherwise:
#		ERR_BUCKET_NOT_FOUND if bucket not found
#		ERR_MISSING_DEPENDENCY if bucket is a file, not a dir
def bucket_size(buckethash):
	if bucket_find(buckethash):
		bucketpath = bucket_getpath(buckethash)
		if os.path.isdir(bucketpath):
			total_size = 0
			for dirpath, dirnames, filenames in os.walk(bucketpath):
				for f in filenames:
					fp = os.path.join(dirpath, f)
					# skip if it is symbolic link
					if not os.path.islink(fp):
						total_size += os.path.getsize(fp)
			return total_size
		else:
			error.exit(error.ERR_MISSING_DEPENDENCY)
	else:
		error.exit(error.ERR_BUCKET_NOT_FOUND)


# Get complete path to file on currently active cache
#   Returns absolute path string
def file_getpath(buckethash, filehash):
	return bucket_getpath(buckethash)+"/"+filehash
	
	
# Generate the actual hashsalt as used in the cachestore
#	Returns string
def file_generatesalt(filename, filesize):
	return filename + ":" + filesize.__str__()
	
	
# Generate the actual filehash as used in the cachestore
#	Returns 32byte hash string
def file_generatehash(hashsalt):
	return hashlib.md5(hashsalt).hexdigest()


# Compute bucketname file name + size
#   Is currently MD5 sum based, may change at later date to reduce clashes.
def file_getnamehash(filepath, filename=None):	
	if os.path.isfile(filepath):
		filesize = os.path.getsize(filepath)
		if filename == None:
			filename = os.path.basename(filepath)
		hashsalt  = file_generatesalt(filename, filesize)
		return file_generatehash(hashsalt)
	error.exit(error.ERR_FILE_NOT_FOUND)


def file_put(buckethash, filepath, forcedname=None):
	utils.root_check()
	filehash = file_getnamehash(filepath, forcedname)
	write_enable()
	shutil.copy(filepath, file_getpath(buckethash, filehash))
	write_disable()
	return filehash


def file_get():
	utils.root_check()
	
	
def file_delete(buckethash, filehash):
	utils.root_check()
	filepath = file_getpath(buckethash, filehash)
	if os.path.exists(filepath):
		write_enable()
		os.remove(filepath)
		write_disable()
		return
	error.exit(error.ERR_FILE_NOT_FOUND)