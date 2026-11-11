#!/usr/bin/python

from fs_lib import *

@struct_printer
def pp_struct_mnt_namespace(mnt_ns, rlvl, ilvl):

	pp_struct_member(mnt_ns, "root", rlvl=rlvl, ilvl=ilvl)

	if ppstruct_vars.pp_struct_opts.counts:
		print("{ind}{c}".format(indent_str(ilvl), c=pp_member_val(mnt_ns, "count")))


if __name__ == "__main__":
	program_display_struct(pp_struct_mnt_namespace)

# vim: sw=4 ts=4 noexpandtab
