#!/usr/bin/python

from fs_lib import *

@struct_printer
def pp_struct_nameidata(ni, rlvl, ilvl):
	pp_struct_member(ni, "path", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(ni, "root", rlvl=rlvl, ilvl=ilvl)

	# flags
	# last_type
	# depth
	# saved_names
	# open_intent

if __name__ == "__main__":
	program_display_struct(pp_struct_nameidata)

# vim: sw=4 ts=4 noexpandtab
