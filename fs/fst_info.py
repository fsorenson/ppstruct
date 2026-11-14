#!/usr/bin/python

from fs_lib import readSU, container_of, long

fst_info = {
	'9p' : {
		's_fs_info'		: 'v9fs_session_info',
		'inode_type'	: 'v9fs_inode',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'adfs' : {
		's_fs_info'		: 'adfs_sb_info',
		'inode_type'	: 'adfs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'affs' : {
		's_fs_info'		: 'affs_sb_info',
		'inode_type'	: 'affs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'afs' : {
		's_fs_info'		: 'afs_super_info',
		'inode_type'	: 'afs_vnode',
		'inode_member'	: ('netfs.inode', 'vfs_inode'),
		'ino_embedded'	: True,
	},
	'aio' : {
		'inode_type'	: 'aio_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'anon_inodefs' : {
		'ino_embedded'	: False,
	},
	'autofs' : {
		's_fs_info'		: 'autofs_sb_info',
		'inode_type'	: 'autofs_info',
		'inode_member'	: 'inode',
		'ino_embedded'	: False,
	},
	'bdev' : {
		'inode_type'	: 'bdev_inode',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'befs' : {
		's_fs_info'		: 'befs_sb_info',
		'inode_type'	: 'befs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'bfs' : {
		's_fs_info'		: 'bfs_sb_info',
		'ino_embedded'	: False,
	},
	'binder' : {
		's_fs_info'		: 'binderfs_info',
		'ino_embedded'	: False,
	},
	'binfmt_misc' : {
		's_fs_info'		: 'user_namespace',
		'ino_embedded'	: False,
	},
	'bpf' : {
		's_fs_info'		: 'bpf_mount_opts',
		'inode_type'	: 'bpf_fs_inode',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'btrfs' : {
		's_fs_info'		: 'btrfs_fs_info',
		'inode_type'	: 'btrfs_inode',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'ceph' : {
		's_fs_info'		: 'ceph_fs_client',
		'inode_type'	: 'ceph_inode_info',
		'inode_member'	: ('netfs.inode', 'vfs_inode'),
		'ino_embedded'	: True,
	},
	'cgroup' : {
		's_fs_info'		: 'cgroup_root',
		'ino_embedded'	: False,
	},
	'cgroup2' : {
		's_fs_info'		: 'cgroup_root',
		'ino_embedded'	: False,
	},
	'cifs' : {
		's_fs_info'		: 'cifs_sb_info',
		'inode_type'	: 'cifsInodeInfo',
		'inode_member'	: ('netfs.inode', 'vfs_inode'),
		'ino_embedded'	: True,
	},
	'smb3' : {
		's_fs_info'		: 'cifs_sb_info',
		'inode_type'	: 'cifsInodeInfo',
		'inode_member'	: ('netfs.inode', 'vfs_inode'),
		'ino_embedded'	: True,
	},
	'coda' : {
		's_fs_info'		: 'venus_comm',
		'inode_type'	: 'coda_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'configfs' : {
		'ino_embedded'	: False,
	},
	'cpuset' : {
		's_fs_info'		: 'cgroup_root',
		'ino_embedded'	: False,
	},
	'cramfs' : {
		's_fs_info'		: 'cramfs_sb_info',
		'ino_embedded'	: False,
	},
	'dax' : {
		'inode_type'	: 'dax_device',
		'inode_member'	: 'inode',
		'ino_embedded'	: True,
	},
	'debugfs' : {
		's_fs_info'		: 'debugfs_fs_info',
		'inode_type'	: 'debugfs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'devpts' : {
		's_fs_info'		: 'pts_fs_info',
		'ino_embedded'	: False,
	},
	'devtmpfs' : {
		'ino_embedded'	: False,
	},
	'ecryptfs' : {
		's_fs_info'		: 'ecryptfs_sb_info',
		'inode_type'	: 'ecryptfs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'efivarfs' : {
		's_fs_info'		: 'efivarfs_fs_info',
		'inode_type'	: 'efivar_entry',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'efs' : {
		's_fs_info'		: 'efs_sb_info',
		'inode_type'	: 'efs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'erofs' : {
		's_fs_info'		: 'erofs_sb_info',
		'inode_type'	: 'erofs_inode',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'exfat' : {
		's_fs_info'		: 'exfat_sb_info',
		'inode_type'	: 'exfat_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'ext2' : {
		's_fs_info'		: 'ext2_sb_info',
		'inode_type'	: 'ext2_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'ext3' : {
		's_fs_info'		: 'ext3_sb_info',
		'inode_type'	: 'ext3_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'ext4' : {
		's_fs_info'		: 'ext4_sb_info',
		'super_fs_info'	: 'ext4_sb_info',
		'inode_type'	: 'ext4_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'f2fs' : {
		's_fs_info'		: 'f2fs_sb_info',
		'inode_type'	: 'f2fs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'fat' : {
		's_fs_info'		: 'msdos_sb_info',
		'inode_type'	: 'msdos_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'vfat' : {
		's_fs_info'		: 'msdos_sb_info',
		'inode_type'	: 'msdos_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'msdos' : {
		's_fs_info'		: 'msdos_sb_info',
		'inode_type'	: 'msdos_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'freevxfs' : {
		's_fs_info'		: 'vxfs_sb_info',
		'inode_type'	: 'vxfs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'fuse' : {
		's_fs_info'		: 'fuse_mount',
		'alt_s_fs_info'	: 'fuse_conn',
		'inode_type'	: 'fuse_inode',
		'inode_member'	: 'inode',
		'ino_embedded'	: True,
	},
	'fuseblk' : {
		's_fs_info'		: 'fuse_mount',
		'alt_s_fs_info'	: 'fuse_conn',
		'inode_type'	: 'fuse_inode',
		'inode_member'	: 'inode',
		'ino_embedded'	: True,
	},
	'fusectl' : {
		's_fs_info'		: 'fuse_conn',
		'ino_embedded'	: False,
	},
	'gfs2' : {
		's_fs_info'		: 'gfs2_sbd',
		'inode_type'	: 'gfs2_inode',
		'inode_member'	: 'i_inode',
		'ino_embedded'	: True,
	},
	'gfs2meta' : {
		's_fs_info'		: 'gfs2_sbd',
		'inode_type'	: 'gfs2_inode',
		'inode_member'	: 'i_inode',
		'ino_embedded'	: True,
	},
	'hfs' : {
		's_fs_info'		: 'hfs_sb_info',
		'inode_type'	: 'hfs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'hfsplus' : {
		's_fs_info'		: 'hfsplus_sb_info',
		'inode_type'	: 'hfsplus_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'hostfs' : {
		's_fs_info'		: 'hostfs_fs_info',
		'inode_type'	: 'hostfs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'hpfs' : {
		's_fs_info'		: 'hpfs_sb_info',
		'inode_type'	: 'hpfs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'hugetlbfs' : {
		's_fs_info'		: 'hugetlbfs_sb_info',
		'inode_type'	: 'hugetlbfs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'iso9660' : {
		's_fs_info'		: 'isofs_sb_info',
		'inode_type'	: 'iso_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'isofs' : {
		's_fs_info'		: 'isofs_sb_info',
		'inode_type'	: 'iso_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'jffs2' : {
		's_fs_info'		: 'jffs2_sb_info',
		'inode_type'	: 'jffs2_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'jfs' : {
		's_fs_info'		: 'jfs_sb_info',
		'inode_type'	: 'jfs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'kernfs' : {
		's_fs_info'		: 'kernfs_super_info',
		'ino_embedded'	: False,
	},
	'minix' : {
		's_fs_info'		: 'minix_sb_info',
		'inode_type'	: 'minix_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'mqueue' : {
		's_fs_info'		: 'ipc_namespace',
		'inode_type'	: 'mqueue_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'nfs' : {
		's_fs_info'		: 'nfs_server',
		'super_fs_info'	: 'nfs_server',
		'inode_type'	: 'nfs_inode',
		'inode_member'	: 'vfs_inode',
		'page_private'	: 'nfs_page',
		'ino_embedded'	: True,
	},
	'nfs4' : {
		's_fs_info'		: 'nfs_server',
		'super_fs_info'	: 'nfs_server',
		'inode_type'	: 'nfs_inode',
		'inode_member'	: 'vfs_inode',
		'page_private'	: 'nfs_page',
		'ino_embedded'	: True,
	},
	'nfsd' : {
		's_fs_info'		: 'net',
		'ino_embedded'	: False,
	},
	'nilfs2' : {
		's_fs_info'		: 'the_nilfs',
		'inode_type'	: 'nilfs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'nsfs' : {
		'ino_embedded'	: False,
	},
	'ntfs' : {
		's_fs_info'		: 'ntfs_volume',
		'inode_type'	: 'big_ntfs_inode',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'ntfs3' : {
		's_fs_info'		: 'ntfs_sb_info',
		'inode_type'	: 'ntfs_inode',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'ocfs2' : {
		's_fs_info'		: 'ocfs2_super',
		'inode_type'	: 'ocfs2_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'ocfs2_dlmfs' : {
		'inode_type'	: 'dlmfs_inode_private',
		'inode_member'	: 'ip_vfs_inode',
		'ino_embedded'	: True,
	},
	'omfs' : {
		's_fs_info'		: 'omfs_sb_info',
		'ino_embedded'	: False,
	},
	'openpromfs' : {
		'inode_type'	: 'op_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'overlay' : {
		's_fs_info'		: 'ovl_fs',
		'inode_type'	: 'ovl_inode',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'pidfs' : {
		'ino_embedded'	: False,
	},
	'pipe' : {
		'inode_type'	: 'pipe_inode_info',
		'inode_member'	: 'inode',
		'ino_embedded'	: False,
	},
	'pipefs' : {
		'inode_type'	: 'pipe_inode_info',
		'inode_member'	: 'inode',
		'ino_embedded'	: False,
	},
	'proc' : {
		's_fs_info'		: 'proc_fs_info',
		'alt_s_fs_info'	: 'pid_namespace',
		'inode_type'	: 'proc_inode',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'pstore' : {
		's_fs_info'		: 'pstore_info',
		'ino_embedded'	: False,
	},
	'pvfs2' : {
		's_fs_info'		: 'orangefs_sb_info_s',
		'inode_type'	: 'orangefs_inode_s',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'orangefs' : {
		's_fs_info'		: 'orangefs_sb_info_s',
		'inode_type'	: 'orangefs_inode_s',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'qnx4' : {
		's_fs_info'		: 'qnx4_sb_info',
		'inode_type'	: 'qnx4_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'qnx6' : {
		's_fs_info'		: 'qnx6_sb_info',
		'inode_type'	: 'qnx6_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'ramfs' : {
		's_fs_info'		: 'ramfs_fs_info',
		'ino_embedded'	: False,
	},
	'resctrl' : {
		's_fs_info'		: 'resctrl_fs_context',
		'ino_embedded'	: False,
	},
	'romfs' : {
		'inode_type'	: 'romfs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'rpc_pipefs' : {
		's_fs_info'		: 'net',
		'inode_type'	: 'rpc_inode',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'securityfs' : {
		'ino_embedded'	: False,
	},
	'selinuxfs' : {
		's_fs_info'		: 'selinux_fs_info',
		'ino_embedded'	: False,
	},
	'shmem' : {
		's_fs_info'		: 'shmem_sb_info',
		'inode_type'	: 'shmem_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'tmpfs' : {
		's_fs_info'		: 'shmem_sb_info',
		'inode_type'	: 'shmem_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'smackfs' : {
		'ino_embedded'	: False,
	},
	'sockfs' : {
		's_fs_info'		: 'net',
		'inode_type'	: 'socket_alloc',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'squashfs' : {
		's_fs_info'		: 'squashfs_sb_info',
		'inode_type'	: 'squashfs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'sysfs' : {
		's_fs_info'		: 'kernfs_super_info',
		'ino_embedded'	: False,
	},
	'sysv' : {
		's_fs_info'		: 'sysv_sb_info',
		'inode_type'	: 'sysv_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'tracefs' : {
		's_fs_info'		: 'tracefs_fs_info',
		'inode_type'	: 'tracefs_inode',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'ubifs' : {
		's_fs_info'		: 'ubifs_info',
		'inode_type'	: 'ubifs_inode',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'udf' : {
		's_fs_info'		: 'udf_sb_info',
		'inode_type'	: 'udf_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'ufs' : {
		's_fs_info'		: 'ufs_sb_info',
		'inode_type'	: 'ufs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'vboxsf' : {
		's_fs_info'		: 'vboxsf_sbi',
		'inode_type'	: 'vboxsf_inode',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'virtiofs' : {
		's_fs_info'		: 'fuse_mount',
		'alt_s_fs_info'	: 'fuse_conn',
		'inode_type'	: 'fuse_inode',
		'inode_member'	: 'inode',
		'ino_embedded'	: True,
	},
	'vxfs' : {
		's_fs_info'		: 'vxfs_sb_info',
		'inode_type'	: 'vxfs_inode_info',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
	'xfs' : {
		's_fs_info'		: 'xfs_mount',
		'super_fs_info'	: 'xfs_mount',
		'inode_type'	: 'xfs_inode',
		'inode_member'	: 'i_vnode',
		'ino_embedded'	: True,
	},
	'zonefs' : {
		's_fs_info'		: 'zonefs_sb_info',
		'inode_type'	: 'zonefs_inode_info',
		'inode_member'	: 'i_vnode',
		'ino_embedded'	: True,
	},
}

filesystem_specific_inode_info = {
	'pipe' : {
		'inode_type'	: 'pipe_inode_info',
		'inode_member'	: 'inode',
		'ino_embedded'	: False,
	},
	'bdev' : {
		'inode_type'	: 'bdev_inode',
		'inode_member'	: 'vfs_inode',
		'ino_embedded'	: True,
	},
}

def get_filesystem_sfsi_type(fstype_name):
	try:
		this_fst_info = fst_info.get(fstype_name)
		if this_fst_info is not None and this_fst_info.get('s_fs_info') is not None:
			return this_fst_info['s_fs_info']
	except:
		pass
	return None

def container_of_cast(addr, struct, member):
	if isinstance(member, (list, tuple)):
		for m in member:
			try:
				return readSU("struct " + struct, container_of(long(addr), "struct " + struct, m))
			except:
				pass
		return None
	return readSU("struct " + struct, container_of(long(addr), "struct " + struct, member))

def get_filesystem_inode(addr, fstype_name=None):
	if not addr:
		return None
	try:
		if fstype_name is None:
			if hasattr(addr, 'i_sb') and addr.i_sb:
				fstype_name = addr.i_sb.s_type.name
			else:
				inode = readSU("struct inode", long(addr))
				fstype_name = inode.i_sb.s_type.name

		this_fst_info = fst_info.get(fstype_name)
		if this_fst_info is None:
			this_fst_info = filesystem_specific_inode_info.get(fstype_name)

		if this_fst_info:
			inode_type = this_fst_info.get('inode_type')
			inode_member = this_fst_info.get('inode_member')
			ino_embedded = this_fst_info.get('ino_embedded', True)
			if inode_type and inode_member and ino_embedded:
				return container_of_cast(addr, inode_type, inode_member)
	except:
		pass
	return None

# vim: sw=4 ts=4 noexpandtab
