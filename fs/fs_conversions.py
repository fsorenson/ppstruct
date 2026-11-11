#!/usr/bin/python

from fs_lib import *
#from file import file_get_dentry, file_get_vfsmnt

# 'vfs_inode' - from fs-specific to vfs inode
# 'foo' - from vfs inode to fs-specific (call this what?)

def container_of_cast(addr, struct, member):
	readSU("struct " + struct, container_of(addr, "struct " + struct, member))

filesystem_specific_info = {
	'nfs' : {
		'vfs_inode'			: lambda nfsi: nfsi.vfs_inode,
		'foo'				: lambda i: container_of_cast(i, "nfs_inode", "vfs_inode"),

		'inode_struct'		: 'nfs_inode',
		'inode_member'		: 'vfs_inode',
		'page_private'		: 'nfs_page',
		's_fs_info'			: 'nfs_server' },

	'nfs4' : {
		'inode_struct'		: 'nfs_inode',
		'inode_member'		: 'vfs_inode',
		'page_private'		: 'nfs_page',
		's_fs_info'			: 'nfs_server' },
	'ext2' : {
		'inode_struct'		: 'ext2_inode_info',
		'inode_member'		: 'vfs_inode' },
	'ext3' : {
		'inode_struct'		: 'ext3_inode_info',
		'inode_member'		: 'vfs_inode' },
	'ext4' : {
		'vfs_inode'			: lambda e4ii: e4ii.vfs_inode,
		'foo'				: lambda i: container_of_cast(i, "ext4_inode_info", "vfs_inode",

		'inode_struct'		: 'ext4_inode_info',
		'inode_member'		: 'vfs_inode',
		's_fs_info'			: 'ext4_sb_info' },
	'proc' : {
		'inode_struct'		: 'proc_inode',
		'inode_member'		: 'vfs_inode' },
	'xfs' : {
		'inode_struct'		: 'xfs_inode',
		'inode_member'		: 'i_vnode',
		's_fs_info'			: 'xfs_mount' },
	'autofs' : {
		'inode_struct'		: 'autofs_info',
		'inode_member'		: 'inode',
		'ino_embedded'		: 0 },
	'isofs' : {
		'inode_struct'		: 'iso_inode_info',
		'inode_member'		: 'vfs_inode' },
	'pipe' : {
		'inode_struct'		: 'pipe_inode_info',
		'inode_member'		: 'inode',
		'ino_embedded'		: 0 },
	'bdev' : {
		'inode_struct'		: 'bdev_inode',
		'inode_member'		: 'vfs_inode' },
	'fuse' : {
		'inode_struct'		: 'fuse_inode',
		'inode_member'		: 'inode' },
	'cifs' : {
		'inode_struct'		: 'cifsInodeInfo',
		'inode_member'		: 'vfs_inode' },
}







# vim: sw=4 ts=4 noexpandtab
