#!/usr/bin/python
import pprint
import argparse
import re
import string
import sys
from pykdump.API import *
from fs_lib import *

pp = pprint.PrettyPrinter(indent=4)


def get_struct_type(addr):
    func_name = sys._getframe(1).f_code.co_name
    if func_name.startswith('pp_struct_'):
        return func_name[len("pp_struct_"):]
    return ""

#def cast_pp_func_struct(addr):

#	ret = get_struct_type(
	
#	sbi = readSU("struct ext4_sb_info", addr)



def pp_struct_nfs_fh(addr, rlvl=1, ilvl=0):
	print("(struct nfs_fh *)0x{:016x}".format(addr))

	if rlvl <= 0:
		return

	if addr == 0:
		return

	ilvl += 1
	rlvl -= 1

#   pp.pprint(self)
	this_function_name = sys._getframe().f_code.co_name

	pp.pprint(this_function_name)

#    print("struct type: {}".format(get_struct_type(addr)))

	nfs_fh = readSU("struct nfs_fh", addr)

	s = nfs_fh.size
#	data = nfs_fh.eval("data")
#	data = Addr(nfs_fh.data)
	data = nfs_fh.data

	print("data: {}".format(data))
#	try:
#		mem = bytearray(readmem(nfs_fh.data, s), encoding='ascii')
#	except:
#		mem = bytearray("x"*s, encoding='ascii')
#		pass

	print(" size: {}".format(s))
#	print(" addr: 0x{:016x}".format(data))
	for i in range(0, s - 1):
		print("{:02x}".format(i, data[i]), end='')
	print("")



#	pp_struct_member(sb, "s_type", rlvl=rlvl, ilvl=ilvl)

#	s_flags = sb.s_flags
#	print indent_str(ilvl), ".s_flags = 0x%x - %s" % (s_flags, flags_to_string(s_flags, SB_FLAGS))

#	print indent_str(ilvl), ".s_blocksize = %d" % (sb.s_blocksize)
#	pp_struct_member(sb, "s_root", rlvl=rlvl, ilvl=ilvl)
#	pp_struct_member(sb, "s_bdev", rlvl=rlvl, ilvl=ilvl)
#	pp_struct_member(sb, "s_bdi", rlvl=rlvl, ilvl=ilvl)


#	if member_size("struct super_block", "s_files") != -1:
#		## works through 2.6.36, after which this became per-cpu
#		s_files_len = len(ListHead(sb.s_files))
#		print indent_str(ilvl), ".s_files: list -H 0x%016x (%d entries)" % (Addr(sb.s_files), s_files_len)
#	if member_size("struct super_block", "s_inodes") != -1:
#		s_inodes_len = len(ListHead(sb.s_inodes))
#		print indent_str(ilvl), ".s_inodes: list -H 0x%016x (%d entries)" % (Addr(sb.s_inodes), s_inodes_len)



if __name__ == "__main__":
	for arg in sys.argv:
		addr = get_arg_value(arg)
		if addr != 0:
			pp_struct_nfs_fh(addr,rlvl=DEFAULT_RLVL)

# vim: sw=4 ts=4 noexpandtab
