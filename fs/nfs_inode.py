#!/usr/bin/python

from __future__ import print_function

from fs_lib import *

@struct_printer
def pp_struct_nfs_inode(nfs_inode, rlvl, ilvl):
# nfs_fh
	pp_struct_member(nfs_inode, "fh", rlvl=rlvl, ilvl=ilvl)

	if struct__has_member("nfs_inode", "npages"):
#	if member_size("struct nfs_inode", "npages") != -1:
		print("{}.npages = {}".format(indent_str(ilvl), nfs_inode.npages))

	if struct__has_member("nfs_inode", "open_files"):
#	if member_size("struct nfs_inode", "open_files") != -1:
		open_files_len = len(ListHead(nfs_inode.open_files))
		print("{}.open_files: list -H 0x{a:016x} ({l} entries)".format(indent_str(ilvl), a=Addr(nfs_inode.open_files), l=open_files_len))

	pp_struct_member(nfs_inode, "vfs_inode", rlvl=rlvl, ilvl=ilvl)

	print("{}.silly_count = {}".format(indent_str(ilvl), nfs_inode.silly_count.counter), end="")
	if nfs_inode.silly_count.counter > 0:
		print(" - list -H 0x{:016x}".format(nfs_inode.silly_list))
	else:
		print


if __name__ == "__main__":
	program_display_struct(pp_struct_nfs_inode)

# vim: sw=4 ts=4 noexpandtab
