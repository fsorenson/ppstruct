#!/usr/bin/python
import pprint
import argparse
import re
import string
import sys
from pykdump.API import *
from fs_lib import *

# from include/linux/mount.h
MNT_FLAGS_C = '''
#define MNT_NOSUID      0x01
#define MNT_NODEV       0x02
#define MNT_NOEXEC      0x04
#define MNT_NOATIME     0x08
#define MNT_NODIRATIME  0x10
#define MNT_RELATIME    0x20
#define MNT_READONLY    0x40    /* does the user want this to be r/o? */
#define MNT_SHRINKABLE  0x100
#define MNT_WRITE_HOLD  0x200
#define MNT_SHARED      0x1000  /* if the vfsmount is a shared mount */
#define MNT_UNBINDABLE  0x2000  /* if the vfsmount is a unbindable mount */
#define MNT_INTERNAL    0x4000
#define MNT_LOCK_READONLY       0x400000
#define MNT_MARKED              0x4000000
'''
MNT_FLAGS = CDefine(MNT_FLAGS_C)

mnt_flags_string_pairs = [
	(MNT_FLAGS.MNT_NOSUID,     'nosuid',     'suid'),
	(MNT_FLAGS.MNT_NODEV,      'nodev',      'dev'),
	(MNT_FLAGS.MNT_NOEXEC,     'noexec',     'exec'),
	(MNT_FLAGS.MNT_NOATIME,    'noatime',    'atime'),
	(MNT_FLAGS.MNT_NODIRATIME, 'nodiratime', 'diratime'),
	(MNT_FLAGS.MNT_RELATIME,   'relatime',   ''),
	(MNT_FLAGS.MNT_READONLY,   'ro',         'rw'),
	]

def show_mnt_flags_strings(mf, sep=','):
	parts = [
		set_str if (mf & flag) else unset_str
		for flag, set_str, unset_str in mnt_flags_string_pairs
		]
	return sep.join(filter(None, parts))


#filesystem_specific_inode_info = {

#'nfs' : {
#'inode_type'    : 'nfs_inode',
#'inode_member'  : 'vfs_inode',
#'page_private'  : 'nfs_page',
#'super_fs_info' : 'nfs_server' },
#'nfs4' : {
#'inode_type'    : 'nfs_inode',
#'inode_member'  : 'vfs_inode',
#'page_private'  : 'nfs_page',
#'super_fs_info' : 'nfs_server' },




# vim: sw=4 ts=4 noexpandtab
