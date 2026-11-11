#!/usr/bin/python

from fs_lib import *
from fs import fst_info
from fs.fst_info import *

SB_FLAGS_C = '''
#define MS_RDONLY	0
#define MS_NOSUID	1
#define MS_NODEV	2
#define MS_NOEXEC	3
#define MS_SYNCHRONOUS	4
#define MS_REMOUNT	5
#define MS_MANDLOCK	6
#define MS_DIRSYNC	7
#define MS_NOATIME	10
#define MS_NODIRATIME	11
#define MS_BIND		12
#define MS_MOVE		13
#define MS_REC		14
#define MS_VERBOSE	15

#define MS_SILENT	15
#define MS_POSIXACL	16
#define MS_UNBINDABLE	17
#define MS_PRIVATE	18
#define MS_SLAVE	19
#define MS_SHARED	20
#define MS_RELATIME	21
#define MS_KERNMOUNT	22
#define MS_I_VERSION	23
#define MS_STRICTATIME	24
#define MS_SNAP_STABLE	27
#define MS_BORN		29
#define MS_ACTIVE	30
#define MS_NOUSER	31
'''
SB_FLAGS = CDefine(SB_FLAGS_C)


def super_block__file_system_type_string(addr):
	try:
		from file_system_type import file_system_type__string
		sb = addr_struct_obj("super_block", addr)
		return file_system_type__string(sb.s_type)
	except:
		return "Unknown in super_block"


# super_block mount options
# RDONLY, NOSUID, NODEV, etc.

def show_sb_opts(sb_addr):
	sb = addr_struct_obj("super_block", sb_addr)
	



@struct_label_string("s_id")
@struct_printer
def pp_struct_super_block(sb, rlvl, ilvl):

	pp_struct_member(sb, "s_type", rlvl=rlvl, ilvl=ilvl)

#	filesystem_type_name = file_system_type__string(
#	filesystem_type_name = file_system_type__string(

	t_name = sb.s_type.name
	sfsi_type = get_filesystem_sfsi_type(t_name)

	if sfsi_type:
		print("{} filesystem type '{}' has s_fs_info of type '{}'".format(indent_str(ilvl), t_name, sfsi_type))
		pp_struct(sfsi_type, sb.s_fs_info, ilvl=ilvl+1, rlvl=rlvl-1)


	s_flags = sb.s_flags
	print("{}.s_flags = 0x{f:016x} - {s}".format(indent_str(ilvl), f=s_flags, s=flags_to_string(s_flags, SB_FLAGS)))

	print("{}.s_blocksize = {}".format(indent_str(ilvl), sb.s_blocksize))
	pp_struct_member(sb, "s_root", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(sb, "s_bdev", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(sb, "s_bdi", rlvl=rlvl, ilvl=ilvl)


	if struct__has_member("super_block", "s_files"):
		## works through 2.6.36, after which this became per-cpu
		## then the list was removed altogether in
		##    upstream 3.13
		##    RHEL 3.10.0-206.el7
		##
		## FIXME: the per-cpu list is not implemented here
		s_files_len = len(ListHead(sb.s_files))
		print("{}.s_files: list -H 0x{a:016x} ({l} entries)".format(indent_str(ilvl), a=Addr(sb.s_files), l=s_files_len))
	if struct__has_member("super_block", "s_inodes"):
		s_inodes_len = len(ListHead(sb.s_inodes))
		print("{}.s_inodes: list -H 0x{a:016x} -o inode.i_sb_list ({l} 'struct inode *' entries)".format(indent_str(ilvl), a=Addr(sb.s_inodes), l=s_inodes_len))


def call_foreach_argv1b(func):
	for arg in sys.argv:
		addr = get_arg_value(arg)
		if addr != 0:
			func(addr, rlvl=DEFAULT_RLVL)

def program_display_struct1b(struct_func):
	call_foreach_argv1b(struct_func)



if __name__ == "__main__":
	program_display_struct(pp_struct_super_block)


# vim: sw=4 ts=4 noexpandtab
