#!/usr/bin/python
from __future__ import print_function
from fs_lib import *

@struct_printer
def pp_struct_loop_device(ldev, rlvl, ilvl):
	print(indent_str(ilvl), "loop {} - {}".format(ldev.lo_number, ldev.lo_file_name))
	print(indent_str(ilvl), ".lo_offset={}, .lo_sizelimit={}, lo_blocksize={}".format(ldev.lo_offset, ldev.lo_sizelimit, ldev.lo_blocksize))


	pp_struct_member(ldev, "lo_backing_file", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(ldev, "lo_device", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(ldev, "lo_disk", rlvl=rlvl, ilvl=ilvl)


if __name__ == "__main__":
	program_display_struct(pp_struct_loop_device)

# vim: sw=4 ts=4 noexpandtab
