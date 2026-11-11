#!/usr/bin/python

#from fs_lib import *

fst_info = {
	'xfs' : {
		's_fs_info'		: 'xfs_mount',
		'super_fs_info'	: 'xfs_mount',
		'inode_type'	: 'xfs_inode',
		'inode_member'	: 'i_vnode',
	},
	'nfs' : {
		's_fs_info'		: 'nfs_server',
		'super_fs_info'	: 'nfs_server',
		'inode_type'	: 'nfs_inode',
		'inode_member'	: 'vfs_inode',
		'page_private'	: 'nfs_page',
	},
	'nfs4' : {
		's_fs_info'		: 'nfs_server',
		'super_fs_info'	: 'nfs_server',
		'inode_type'	: 'nfs_inode',
		'inode_member'	: 'vfs_inode',
		'page_private'	: 'nfs_page',
	},
	'nfsd' : {
		's_fs_info' : 'net',
	},
	'cifs' : {
		's_fs_info'		: 'cifs_sb_info',
		'inode_type'	: 'cifsInodeInfo',
		'inode_member'	: 'vfs_inode',
	},
	'ext4' : {
		's_fs_info'		: 'ext4_sb_info',
		'super_fs_info'	: 'ext4_sb_info',
		'inode_type'	: 'ext4_inode_info',
		'inode_member'	: 'vfs_inode',
	},
	'ext3' : {
		's_fs_info'		: 'ext3_sb_info',
		'inode_type'	: 'ext3_inode_info',
		'inode_member'	: 'vfs_inode',
	},
	'ext2' : {
		's_fs_info'		: 'ext2_sb_info',
		'inode_type'	: 'ext2_inode_info',
		'inode_member'	: 'vfs_inode',
	},
	'sysfs' : {
		's_fs_info' : 'kernfs_super_info',
	},
	'kernfs' : {
		's_fs_info' : 'kernfs_super_info'
	},
	'vfat' : {
		's_fs_info' : 'msdos_sb_info',
	},
	'autofs' : {
		's_fs_info'		: 'autofs_sb_info',
		'inode_type'	: 'autofs_info',
		'inode_member'	: 'inode',
		'ino_embedded'	: 0,
	},
	'devpts' : {
		's_fs_info' : 'pts_fs_info',
	},
	'debugfs' : {
		's_fs_info' : 'debugfs_fs_info',
	},
	'devtmpfs' : {
	},
	'efivarfs' : {
	},
	'fuse' : {
		's_fs_info'		: 'fuse_conn',
		'inode_type'	: 'fuse_inode',
		'inode_member'	: 'inode',
	},
	'hugetlbfs' : {
		's_fs_info' : 'hugetlbfs_sb_info',
	},
	'shmem' : {
	},
	'tmpfs' : {
	},
	'securityfs' : {
	},
	'rpc_pipefs' : {
		's_fs_info' : 'net',
	},
	'pstore' : {
	},
	'proc' : {
		's_fs_info'		: 'pid_namespace',
		'inode_type'	: 'proc_inode',
		'inode_member'	: 'vfs_inode',
	},
	'cpuset' : {
	},
	'cgroup' : {
	},
	'configfs' : {
	},
	'binfmt_misc' : {
	},
	'mqueue' : {
	},
	'btrfs' : {
		's_fs_info' : 'btrfs_fs_info',
	},
	'gfs2' : {
		's_fs_info' : 'gfs2_sbd',
	},
	'overlay' : {
		's_fs_info' : 'ovl_fs',
	},
	'cramfs' : {
		's_fs_info' : 'cramfs_sb_info',
	},
	'squashfs' : {
		's_fs_info' : 'squashfs_sb_info',
	},
	'bfs' : {
		's_fs_info' : 'bfs_sb_info',
	},
	'ceph' : {
		's_fs_info' : 'ceph_fs_client',
	},
	'ocfs2' : {
		's_fs_info' : 'ocfs2_super',
	},
	'jfs' : {
		's_fs_info' : 'jfs_sb_info',
	},
	'isofs' : {
		'inode_type'	: 'iso_inode_info',
		'inode_member'	: 'vfs_inode',
	},
}




filesystem_specific_inode_info = {
	'pipe' : {
		'inode_type'	: 'pipe_inode_info',
		'inode_member'	: 'inode',
		'ino_embedded'	: 0 },
	'bdev' : {
		'inode_type'	: 'bdev_inode',
		'inode_member'	: 'vfs_inode' },
	}

def get_filesystem_sfsi_type(fstype_name):
	try:
		this_fst_info = fst_info[fstype_name]

		if this_fst_info is not None and this_fst_info['s_fs_info'] is not None:
			sfsi_type = this_fst_info['s_fs_info']
			return sfsi_type
	except:
		pass
	return None

# vim: sw=4 ts=4 noexpandtab
