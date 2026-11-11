#!/usr/bin/python

from fs_lib import *

D_FLAGS_C = '''
#define DCACHE_AUTOFS_PENDING	0
#define DCACHE_NFSFS_RENAMED	1
#define DCACHE_DISCONNECTED	2
#define DCACHE_REFERENCED	3
#define DCACHE_UNHASHED		4
#define DCACHE_INOTIFY_PARENT_WATCHED	5
#define DCACHE_COOKIE		6
#define DCACHE_FSNOTIFY_PARENT_WATCHED	7
#define DCACHE_MOUNTED		16
#define DCACHE_NEED_AUTOMOUNT	17
#define DCACHE_MANAGE_TRANSIT	18
'''
D_FLAGS = CDefine(D_FLAGS_C)

@struct_label_string("d_name")
@struct_printer
def pp_struct_dentry(dentry, rlvl, ilvl):
#	print("{}.d_name = %s".format(indent_str(ilvl), qstr(dentry.d_name)))

	d_flags = dentry.d_flags
	print("{}.d_flags = 0x{fl:x} - {str}".format(indent_str(ilvl), fl=d_flags, str=flags_to_string(d_flags, D_FLAGS)))

	pp_struct_member(dentry, "d_inode", rlvl=rlvl, ilvl=ilvl)

	d_parent = dentry.d_parent
	if (d_parent and (d_parent != dentry)):
		pp_struct_member(dentry, "d_parent", rlvl=rlvl, ilvl=ilvl)

	pp_struct_member(dentry, "d_sb", rlvl=rlvl, ilvl=ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_dentry)

# vim: sw=4 ts=4 noexpandtab
