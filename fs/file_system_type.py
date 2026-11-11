#!/usr/bin/python

from fs_lib import *
#import file_systems from ppstruct_types
#from ppstruct_types import file_systems
#from fs import fst_info


def file_system_type__string(addr):
	try:
		fst = addr_struct_obj("file_system_type", addr)
		return fst.name
	except:
		return "Unknown"

@struct_label_string("name")
@struct_printer
def pp_struct_file_system_type(fst, rlvl, ilvl):

#	print indent_str(ilvl), ".name = '%s'" % fst.name
	pp_struct_member(fst, "owner", rlvl=rlvl, ilvl=ilvl)

	try:
		fst_name = file_system_type__string(fst)

		this_fst_info = fst_info[fst_name]
		if this_fst is not None and this_fst_info.s_fs_info is not None:
			print("displaying fst {}".format(fst_name))
			pp_struct(this_fst_info, fst, rlvl=rlvl, ilvl=ilvl)
	except:
		pass

if __name__ == "__main__":
	program_display_struct(pp_struct_file_system_type)

# vim: sw=4 ts=4 noexpandtab
