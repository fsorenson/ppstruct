#!/usr/bin/python

from __future__ import print_function

from fs_lib import *
from fs.fst_info import get_filesystem_inode


INO_STATE_C = '''
#define DIRTY_SYNC 0
#define DIRTY_DATASYNC 1
#define DIRTY_PAGES 2
#define NEW 3
#define WILL_FREE 4
#define FREEING 5
#define CLEAR 6
#define LOCK 7
#define SYNC 8
'''

# RHEL 7 kernel, beginning with kernel-3.10.0-263.el7
INO_STATE_C_RHEL7 = '''
#define DIRTY_SYNC 0
#define DIRTY_DATASYNC 1
#define DIRTY_PAGES 2
#define NEW 3
#define WILL_FREE 4
#define FREEING 5
#define CLEAR 6
#define SYNC 7
#define REFERENCED 8
#define DIO_WAKEUP 9
#define LINKABLE 10
'''

INO_STATE = CDefine(INO_STATE_C_RHEL7)

INO_FLAGS_C = '''
#define SYNC 0
#define NOATIME 1
#define APPEND 2
#define IMMUTABLE 3
#define DEAD 4
#define NOQUOTA 5
#define DIRSYNC 6
#define NOCMTIME 7
#define SWAPFILE 8
#define PRIVATE 9
#define AUTOMOUNT 11
#define AOP_EXT 14 /* in RHEL6, but not RHEL7 */
'''
# not included:
#  IMA (1<<10) in RHEL7 and upstream, but not RHEL6
#  NOSEC (1<<12)in RHEL7 and upstream, but not RHEL6
#  IOPS_WRAPPER 13 /* in RHEL7, but not RHEL6 or upstream */
#  AOP in RHEL7, but not RHEL6 or upstream
#  DAX is 16384 in RHEL7, 8192 in upstream

INO_FLAGS = CDefine(INO_FLAGS_C)

def inode_mode_type_char(mode):
	ret = '?'
	if (S_ISREG(mode)): ret = '-'
	elif (S_ISSOCK(mode)): ret = 's'
	elif (S_ISLNK(mode)): ret = 'l'
	elif (S_ISBLK(mode)): ret = 'b'
	elif (S_ISDIR(mode)): ret = 'd'
	elif (S_ISCHR(mode)): ret = 'c'
	elif (S_ISFIFO(mode)): ret = 'p'
	return ret

def inode_mode_type_string(mode):
	ret = '???'
	if (S_ISREG(mode)): ret = 'REG'
	elif (S_ISSOCK(mode)): ret = 'SOCK'
	elif (S_ISLNK(mode)): ret = 'LNK'
	elif (S_ISBLK(mode)): ret = 'BLK'
	elif (S_ISDIR(mode)): ret = 'DIR'
	elif (S_ISCHR(mode)): ret = 'CHR'
	elif (S_ISFIFO(mode)): ret = 'FIFO'
	return ret

__mbits = ['---', '--x', '-w-', '-wx', 'r--', 'r-x', 'rw-', 'rwx']

def mode_bits_string(mode):
	oth = list(__mbits[mode &  7])
	grp = list(__mbits[(mode >> 3) & 7])
	usr = list(__mbits[(mode >> 6) & 7])
	if (mode & S_ISUID):
		if (usr[2] == 'x'): usr[2] = 's'
		else: usr[2] = 'S'
	if (mode & S_ISGID):
		if (grp == 'x'): grp[2] = 's'
		else: grp[2] = 'S'
	if (mode & S_ISVTX):
		if (oth[2] == 'x'): oth[2] = 't'
		else: oth[2] = 'T'
	return "{}".format("".join(usr + grp + oth))
#	return "%s%s%s" % (usr, grp, oth)


filesystem_specific_inode_info = {
		'nfs' : {
			'inode_type'	: 'nfs_inode',
			'inode_member'	: 'vfs_inode',
			'page_private'	: 'nfs_page',
			'super_fs_info'	: 'nfs_server' },
		'nfs4' : {
			'inode_type'	: 'nfs_inode',
			'inode_member'	: 'vfs_inode',
			'page_private'	: 'nfs_page',
			'super_fs_info'	: 'nfs_server' },
		'ext2' : {
			'inode_type'	: 'ext2_inode_info',
			'inode_member'	: 'vfs_inode' },
		'ext3' : {
			'inode_type'	: 'ext3_inode_info',
			'inode_member'	: 'vfs_inode' },
		'ext4' : {
			'inode_type'	: 'ext4_inode_info',
			'inode_member'	: 'vfs_inode',
			'super_fs_info'	: 'ext4_sb_info' },
		'proc' : {
			'inode_type'	: 'proc_inode',
			'inode_member'	: 'vfs_inode' },
		'xfs' : {
			'inode_type'	: 'xfs_inode',
			'inode_member'	: 'i_vnode',
			'super_fs_info'	: 'xfs_mount' },
		'autofs' : {
			'inode_type'	: 'autofs_info',
			'inode_member'	: 'inode',
			'ino_embedded'	: 0 },
		'isofs' : {
			'inode_type'	: 'iso_inode_info',
			'inode_member'	: 'vfs_inode' },
		'pipe' : {
			'inode_type'	: 'pipe_inode_info',
			'inode_member'	: 'inode',
			'ino_embedded'	: 0 },
		'bdev' : {
			'inode_type'	: 'bdev_inode',
			'inode_member'	: 'vfs_inode' },
		'fuse' : {
			'inode_type'	: 'fuse_inode',
			'inode_member'	: 'inode' },
		'cifs' : {
			'inode_type'	: 'cifsInodeInfo',
			'inode_member'	: 'vfs_inode' },
		}

# include/linux/hash.h
#GOLDEN_RATIO_PRIME_32 = 0x9e370001UL
#GOLDEN_RATIO_PRIME_64 = 0x9e37fffffffc0001
#GOLDEN_RATIO_PRIME = GOLDEN_RATIO_PRIME_64
#GOLDEN_RATIO_PRIME_32 = 0x9e370001
#GOLDEN_RATIO_PRIME_64 = 0x9e37fffffffc0001
#GOLDEN_RATIO_PRIME = GOLDEN_RATIO_PRIME_64

# arch/*/include/asm/cache.h
#L1_CACHE_SHIFT = 6
#L1_CACHE_BYTES = (1 << L1_CACHE_SHIFT)

# fs/inode.c
# #define I_HASHBITS i_hash_shift
# #define I_HASHMASK i_hash_mask

def inode_hash(sb, hashval):
	GOLDEN_RATIO_PRIME_32 = 0x9e370001
	GOLDEN_RATIO_PRIME_64 = 0x9e37fffffffc0001
	GOLDEN_RATIO_PRIME = GOLDEN_RATIO_PRIME_64
	L1_CACHE_SHIFT = 6
	L1_CACHE_BYTES = (1 << L1_CACHE_SHIFT)

	tmp = (hashval * sb) ^ (GOLDEN_RATIO_PRIME + hashval) / L1_CACHE_BYTES
	tmp = tmp ^ ((tmp ^ GOLDEN_RATIO_PRIME) >> readSymbol("i_hash_shift"))
	return tmp & readSymbol("i_hash_mask")


# TODO
# udf - udf_inode_info
# ufs - ufs_inode_info
# ubifs - ubifs_inode
# sysv - sysv_inode
# squashfs - squashfs_inode_info
# sysfs - 
# devtmpfs
# romfs
# ocfs2
# jbd2 - jbd2_inode
# jfs - jfs_inode_info
# jffs2
# gfs2 - gfs2_inode
# fat - msdos_inode_info
# btrfs
# hostfs - hostfs_inode_info

def pp_filesystem_specific_inode(addr, rlvl=1, ilvl=1):
	print("(struct inode *)0x{addr:016x}".format(addr=addr))

	if addr == 0 or rlvl <= 0:
		return

	ilvl += 1
	rlvl -= 1
#
#	inode = addr_struct_obj("inode", addr)
#	if inode != None: sb = 
#def addr_struct_obj(struct_name, addr):
#
#
#	#filesystem_specific_inode_info
#
#filesystem_specific_inode_info = {
#	'nfs' : {
#		'inode_type'    : 'nfs_inode',
#		'inode_member'  : 'vfs_inode' },
#		'super_fs_info' : 'nfs_server' },

def inode__file_system_type_string(addr):
	try:
		from super_block import super_block__file_system_type_string
		inode = addr_struct_obj("inode", addr)
		return super_block__file_system_type_string(inode.i_sb)
	except:
		return "Unknown"

@struct_printer
def pp_struct_inode(inode, rlvl, ilvl):

	print("{}.i_ino = {ino}, .i_size = {s}, .i_nlink = {nlink}".format(indent_str(ilvl), ino=inode.i_ino, s=inode.i_size, nlink=inode.i_nlink))
	# TODO: human-readable size

	i_mode = inode.i_mode
	itype = i_mode & S_IFMT
	obits = i_mode ^ itype

	mode_string = "%s%s" % (inode_mode_type_char(itype), mode_bits_string(obits))
	print("{}.i_mode = {mode:o} {str}".format(indent_str(ilvl), mode=i_mode, str=mode_string), end='')
	print(", {uid}, {gid}".format(uid=pp_uid(inode.i_uid), gid=pp_gid(inode.i_gid)))

#	print indent_str(ilvl) + ".i_size = %d, .i_uid = %d, .i_gid = %d" % (inode.i_size, inode.i_uid, inode.i_gid)
#	print("{}.i_size = {sz}".format(indent_str(ilvl), sz=inode.i_size), end='')

	print("{}.i_state = 0x{st:x} - {str}".format(indent_str(ilvl), st=inode.i_state, str=flags_to_string(inode.i_state, INO_STATE)))
	print("{}.i_flags = 0x{fl:x} - {str}".format(indent_str(ilvl), fl=inode.i_flags, str=flags_to_string(inode.i_flags, INO_FLAGS)))

	pp_struct_member(inode, "i_sb", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(inode, "i_mapping", rlvl=rlvl, ilvl=ilvl)

	# TODO: filesystem-specific inode info
	#	- nfs - nfs_inode.vfs_inode
	#	- ext4 - ext4_inode_info.vfs_inode
	#	- devtmpfs -
	#	- cgroup
	#	- fuse - fuse_inode.inode
	#	- proc - proc_inode.vfs_inode
	#	- autofs

	pp_struct_member(inode, "i_atime", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(inode, "i_mtime", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(inode, "i_ctime", rlvl=rlvl, ilvl=ilvl)

	# i_atime, i_mtime, i_ctime
	# notify info

	if inode.hasField("i_dentry"):
		i_dentry = inode.i_dentry
		num_dentries = len(ListHead(i_dentry))
		print("{}.i_dentry - list of dentries - 0x{:016x} ({} entries)".format(indent_str(ilvl), i_dentry, num_dentries))

		i = 0
		tmp_dentries = readListByHead(i_dentry)
		for tmp_entry in tmp_dentries:
			i += 1
			try:
#				dentry = readSU("struct dentry", container_of(tmp_entry, "struct_dentry", "d_alias"))
				dentry = list_entry(tmp_entry, "dentry", "d_alias")
				print("{ind}{i} - ".format(ind=indent_str(ilvl), i=i), end='')
				pp_struct("dentry", dentry, rlvl=rlvl, ilvl=ilvl)
			except:
				print("{ind}{i} - unable to display dentry (list_addr = 0x{ent:016x})".format(ind=indent_str(ilvl), i=i, ent=tmp_entry))

	fs_inode = get_filesystem_inode(inode)
	if fs_inode:
		itype = obj__struct_type(fs_inode)
		print("{}{}".format(indent_str(ilvl), fmt_struct_addr(itype, long(fs_inode))))


if __name__ == "__main__":
	program_display_struct(pp_struct_inode)

# vim: sw=4 ts=4 noexpandtab
