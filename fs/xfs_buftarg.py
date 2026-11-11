#!/usr/bin/python
from fs_lib import *



@struct_printer
def pp_struct_xfs_buftarg(xfs_buftarg, rlvl, ilvl):
	pp_struct_member(xfs_buftarg, "bt_bdev", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(xfs_buftarg, "bt_bdi", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(xfs_buftarg, "bt_mount", rlvl=rlvl, ilvl=ilvl)

#	block_num = xfs_buftarg.b_bn
#	b_queuetime = xfs_buftarg.b_queuetime
#	b_io_remaining = xfs_buftarg.b_io_remaining

#	print("{}.b_file_offset = {}, .b_buffer_length = {}".format(indent_str(ilvl), xfs_buftarg.b_file_offset, xfs_buftarg.b_buffer_length))
#	print("{}.b_flags = 0x{f:x} - {s}".format(indent_str(ilvl), f=xfs_buftarg.b_flags, s=flags_to_string(xfs_buftarg.b_flags, XFS_BUF_FLAGS)))


#	pp_struct_member(xfs_buftarg, "b_target", rlvl=rlvl, ilvl=ilvl)
#	pp_struct_member(xfs_buftarg, "b_pag", rlvl=rlvl, ilvl=ilvl)



# vim: sw=4 ts=4 noexpandtab
