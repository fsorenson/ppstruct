#!/usr/bin/python
from fs_lib import *

@struct_printer
def pp_struct_ext4_inode_info(e4ii, rlvl, ilvl):
	pp_struct_member(e4ii, "vfs_inode", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(e4ii, "jinode", rlvl=rlvl, ilvl=ilvl)

	pp_struct_member(e4ii, "i_sync_tid", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(e4ii, "i_fdatasync_tid", rlvl=rlvl, ilvl=ilvl)

	# i_disksize


# vim: sw=4 ts=4 noexpandtab
