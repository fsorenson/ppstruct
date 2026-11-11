#!/usr/bin/python
from fs_lib import *

XFS_INO_FLAGS_C_BAD = '''
#define XFS_IRECLAIM            1
#define XFS_ISTALE              2
#define XFS_IRECLAIMABLE        4
#define XFS_INEW                8
#define XFS_ITRUNCATED          32
#define XFS_IDIRTY_RELEASE      64

#define XFS_IFLOCK              128
#define XFS_IPINNED             256
#define XFS_IDONTCACHE          512
'''
XFS_INO_FLAGS_C = '''
#define XFS_IRECLAIM            0
#define XFS_ISTALE              1
#define XFS_IRECLAIMABLE        2
#define XFS_INEW                3
#define XFS_ITRUNCATED          5
#define XFS_IDIRTY_RELEASE      6

#define XFS_IFLOCK              7
#define XFS_IPINNED             8
#define XFS_IDONTCACHE          9
'''
XFS_INO_FLAGS = CDefine(XFS_INO_FLAGS_C)



@struct_printer
def pp_struct_xfs_inode(xfs_inode, rlvl, ilvl):

	print("{}.i_flags = 0x{fl:x} - {str}".format(indent_str(ilvl), fl=xfs_inode.i_flags, str=flags_to_string(xfs_inode.i_flags, XFS_INO_FLAGS)))
	pp_struct_member(xfs_inode, "i_vnode", rlvl=rlvl, ilvl=ilvl)

	pp_struct_member(xfs_inode, "i_mount", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(xfs_inode, "i_udquot", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(xfs_inode, "i_gdquot", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(xfs_inode, "i_pdquot", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(xfs_inode, "i_imap", rlvl=rlvl, ilvl=ilvl)

	pp_struct_member(xfs_inode, "i_df", rlvl=rlvl, ilvl=ilvl)
	if xfs_inode.hasField("i_af"):
		if (xfs_inode.hasField("i_forkoff") and xfs_inode.i_forkoff != 0) or xfs_inode.i_af.if_bytes != 0:
			pp_struct_member(xfs_inode, "i_af", rlvl=rlvl, ilvl=ilvl)
	elif xfs_inode.hasField("i_afp") and long(xfs_inode.i_afp) != 0:
		pp_struct_member(xfs_inode, "i_afp", rlvl=rlvl, ilvl=ilvl)

	if xfs_inode.hasField("i_cowfp") and long(xfs_inode.i_cowfp) != 0:
		pp_struct_member(xfs_inode, "i_cowfp", rlvl=rlvl, ilvl=ilvl)

	pp_struct_member(xfs_inode, "i_itemp", rlvl=rlvl, ilvl=ilvl)
	if xfs_inode.hasField("i_d"):
		pp_struct_member(xfs_inode, "i_d", rlvl=rlvl, ilvl=ilvl)
	else:
		parts = []
		if xfs_inode.hasField("i_disk_size"):
			parts.append(".i_disk_size = {}".format(xfs_inode.i_disk_size))
		if xfs_inode.hasField("i_nblocks"):
			parts.append(".i_nblocks = {}".format(xfs_inode.i_nblocks))
		if xfs_inode.hasField("i_projid"):
			parts.append(".i_projid = {}".format(xfs_inode.i_projid))
		if xfs_inode.hasField("i_extsize"):
			parts.append(".i_extsize = {}".format(xfs_inode.i_extsize))
		if parts:
			print(indent_str(ilvl) + ", ".join(parts))
		if xfs_inode.hasField("i_diflags") and xfs_inode.i_diflags != 0:
			print("{}.i_diflags = 0x{:x}".format(indent_str(ilvl), xfs_inode.i_diflags))
		if xfs_inode.hasField("i_crtime"):
			pp_struct_member(xfs_inode, "i_crtime", rlvl=rlvl, ilvl=ilvl)


# /* Inline data is read in */
XFS_IFINLINE = 1

# try to get the target of an xfs symlink

def xfs_readlink(xfs_inode):
	xfs_inode = readSU("struct xfs_inode", xfs_inode)

	if xfs_inode.hasField("i_d"):
		pathlen = xfs_inode.i_d.di_size
	elif xfs_inode.hasField("i_disk_size"):
		pathlen = xfs_inode.i_disk_size
	elif xfs_inode.hasField("i_vnode"):
		pathlen = xfs_inode.i_vnode.i_size
	else:
		return "UNKNOWN"

	if pathlen <= 0:
		return "UNKNOWN"

	if xfs_inode.hasField("i_df"):
		if xfs_inode.i_df.hasField("if_format"):
			if int(xfs_inode.i_df.if_format) == 1:  # XFS_DINODE_FMT_LOCAL
				return readmem(long(xfs_inode.i_df.if_data), pathlen)
		elif xfs_inode.i_df.hasField("if_flags"):
			if (xfs_inode.i_df.if_flags & XFS_IFINLINE):
				return readmem(long(xfs_inode.i_df.if_u1.if_data), pathlen)

	return "UNKNOWN"


if __name__ == "__main__":
	program_display_struct(pp_struct_xfs_inode)

# vim: sw=4 ts=4 noexpandtab
