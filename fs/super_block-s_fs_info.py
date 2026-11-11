#!/usr/bin/python

from fs_lib import *
from ppstruct_types import fst_info


@struct_printer
def pp_struct_s_fs_info(addr, fst_string, ilvl, rlvl):

	fsti = fst_info[fst_string]
	if fsti is not None:
		if fsti['s_fs_info'] is not None:
			pp_struct(fsti['s_fs_info'], addr, ilvl, rlvl)
		else:
			print("{}(void *)0x{:016x} - s_fs_info is unknown type for file_system_type '{}'".format(indent_str(ilvl), addr, fst_string))
	else:
		print("{}(void *)0x{:016x} - file_system_type '{}' unrecognized".format(indent_str(ilvl), addr))

if __name__ == "__main__":
	if len(sys.argv) == 2:
		addr = get_arg_value(sys.argv[0])
		fst_string = sys.argv[1]
		pp_struct_s_fs_info(addr, fst_string, ilvl=0, rlvl=DEFAULT_RLVL)

# vim: sw=4 ts=4 noexpandtab
