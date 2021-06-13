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


# Compute bucketname from readable name.
#   Is currently MD5 sum based, may change at later date to reduce clashes.
def bucket_getnamehash(name):
	return hashlib.md5(name).hexdigest()


# Create a new bucket.
#	Does not error if already exists.
#	Does not touch bucket if already exists.
def bucket_create(namehash, comment):
	utils.root_check()
	newDB = open(TMPDIR+BUCKETDB,"w")
	if os.path.isfile(CATALOGDIR+BUCKETDB):
		bucketDB = open(CATALOGDIR+BUCKETDB,"r")
		for bucketDBentry in bucketDB:
			bucketEntry = bucketDBentry.split(":")
			if bucketEntry[0] != namehash:
				newDB.write(bucketDBentry)
		bucketDB.close()
		
	newDB.write(namehash + ":" + comment + "\n")
	
	newDB.close()
	
	write_enable()
	if not os.path.isdir(DATADIR+namehash):
		os.mkdir(DATADIR+namehash)
	shutil.move(TMPDIR+BUCKETDB, CATALOGDIR+BUCKETDB)
	write_disable()	


# Touch (aka mark as most recently used) bucket.
#	Generates a ERR_MISSING_DEPENDENCY if DB not found
#	Generates a ERR_BUCKET_NOT_FOUND if Bucket not found
#	Returns True if bucket found, and touched
def bucket_touch(namehash):
	utils.root_check()
	thisBucket = None
	if os.path.isfile(CATALOGDIR+BUCKETDB):
		bucketDB = open(CATALOGDIR+BUCKETDB,"r")
		newDB = open(TMPDIR+BUCKETDB,"w")
		for bucketDBentry in bucketDB:
			bucketEntry = bucketDBentry.split(":")
			if bucketEntry[0] != namehash:
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
def bucket_find(namehash):
	if os.path.isfile(CATALOGDIR+BUCKETDB):
		bucketDB = open(CATALOGDIR+BUCKETDB,"r")
		for bucketDBentry in bucketDB:
			bucketEntry = bucketDBentry.split(":")
			if bucketEntry[0] == namehash:
				bucketDB.close()
				return True
		return False
	else:
		error.exit(error.ERR_MISSING_DEPENDENCY)


# Delete a bucket and its contents.
#	Returns namehash if found.
#	Returns False if not found
#	Generates a ERR_MISSING_DEPENDENCY if DB not found
def bucket_delete(namehash):
	utils.root_check()
	thisBucket = None
	if os.path.isfile(CATALOGDIR+BUCKETDB):
		bucketDB = open(CATALOGDIR+BUCKETDB,"r")
		newDB = open(TMPDIR+BUCKETDB,"w")
		for bucketDBentry in bucketDB:
			bucketEntry = bucketDBentry.split(":")
			if bucketEntry[0] != namehash:
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
	shutil.rmtree(DATADIR+thisBucket[0])
	shutil.move(TMPDIR+BUCKETDB, CATALOGDIR+BUCKETDB)
	write_disable()
	return thisBucket[0]


# Recursively check the size of a bucket.
#	Returns size in bytes if found.
#	Generates an error otherwise:
#		ERR_BUCKET_NOT_FOUND if bucket not found
#		ERR_MISSING_DEPENDENCY if bucket is a file, not a dir
def bucket_size(namehash):
	if bucket_find(namehash):
		bucketpath = DATADIR+namehash
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


def file_get():
	utils.root_check()
	cache.cache_write_enable()
	
	cache.cache_write_disable()


def file_put():
	utils.root_check()


def file_rename():
	utils.root_check()


def file_delete():
	utils.root_check()
	cache.cache_write_enable()
	
	cache.cache_write_disable()