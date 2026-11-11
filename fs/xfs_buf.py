#!/usr/bin/python
from __future__ import print_function
from fs_lib import *

### rhel6 flags...need to check other kernels
# 2.6.32-504.12.2.el6.x86_6
XFS_BUF_FLAGS_C = '''
#define XBF_READ         1
#define XBF_WRITE        2
#define XBF_MAPPED       4
#define XBF_ASYNC        8
#define XBF_DONE         16
#define XBF_DELWRI       32
#define XBF_STALE        64
#define XBF_ORDERED      2048
#define XBF_READ_AHEAD   4096
#define XBF_LOG_BUFFER   8192

#define XBF_LOCK         16384
#define XBF_TRYLOCK      32768
#define XBF_DONT_BLOCK   65536

#define _XBF_PAGES       262144
#define _XBF_RUN_QUEUES  524288
#define _XBF_KMEM        1048576
#define _XBF_DELWRI_Q    2097152
#define _XBF_LRU_DISPOSE 16777216
'''
XFS_BUF_FLAGS = CDefine(XFS_BUF_FLAGS_C)



@struct_printer
def pp_struct_xfs_buf(xfs_buf, rlvl, ilvl):

	block_num = xfs_buf.b_bn
	b_queuetime = xfs_buf.b_queuetime
	b_io_remaining = xfs_buf.b_io_remaining

	print("{}.b_file_offset = {}, .b_buffer_length = {}".format(indent_str(ilvl), xfs_buf.b_file_offset, xfs_buf.b_buffer_length))
	print("{}.b_flags = 0x{f:x} - {s}".format(indent_str(ilvl), f=xfs_buf.b_flags, s=flags_to_string(xfs_buf.b_flags, XFS_BUF_FLAGS)))

#	pp_struct_member(xfs_buf, "b_target", rlvl=rlvl, ilvl=ilvl)
	b_target = xfs_buf.b_target
	print("{}.b_target".format(indent_str(ilvl)), end='')
	pp_struct("xfs_buftarg", b_target, rlvl=rlvl, ilvl=ilvl)

	pp_struct_member(xfs_buf, "b_pag", rlvl=rlvl, ilvl=ilvl)



# vim: sw=4 ts=4 noexpandtab
