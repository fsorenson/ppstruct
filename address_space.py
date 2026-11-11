#!/usr/bin/python
from __future__ import print_function
from fs_lib import *

def address_space__file_system_type_string(addr):
	try:
		from inode import inode__file_system_type_string
		address_space = addr_struct_obj("address_space", addr)
		return inode__file_system_type_string(address_space.host)
	except Exception as err:
		return "Unknown in address_space: {}".format(str(err))

@struct_printer
def pp_struct_address_space(aspace, rlvl, ilvl):

	nrpages = aspace.nrpages
	print("{}.nrpages = {p} = {b} bytes".format(indent_str(ilvl), p=nrpages, b=(nrpages * PAGE_SIZE)))

	if struct__has_member("address_space", "page_tree"):
		page_tree = aspace.page_tree
		print("{}.page_tree: tree -t ra 0x{a:016x}".format(indent_str(ilvl), a=aspace.page_tree))
	elif struct__has_member("address_space", "i_pages"):
		i_pages = aspace.i_pages
		print("{}.i_pages: tree -t ra 0x{a:016x}".format(indent_str(ilvl), a=aspace.i_pages))


	pp_struct_member(aspace, "host", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(aspace, "backing_dev_info", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(aspace, "assoc_mapping", rlvl=rlvl, ilvl=ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_address_space)

# vim: sw=4 ts=4 noexpandtab
