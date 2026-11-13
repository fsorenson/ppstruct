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

	tree_type_flags = {
		'radix_tree_root': 'ra',
		'xarray': 'x',
	}

	tree_member = None
	if struct__has_member("address_space", "page_tree"):
		tree_member = "page_tree"
	elif struct__has_member("address_space", "i_pages"):
		tree_member = "i_pages"

	if tree_member:
		tree_obj = getattr(aspace, tree_member)
		flag = tree_type_flags.get(obj__struct_type(tree_obj), 'x' if obj__struct_type(tree_obj) == 'xarray' else 'ra')
		print("{ind}.{mbr}: tree -t {flag} 0x{a:016x}".format(
			ind=indent_str(ilvl), mbr=tree_member, flag=flag, a=tree_obj))


	pp_struct_member(aspace, "host", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(aspace, "backing_dev_info", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(aspace, "assoc_mapping", rlvl=rlvl, ilvl=ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_address_space)

# vim: sw=4 ts=4 noexpandtab
