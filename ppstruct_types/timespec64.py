#!/usr/bin/python

from __future__ import print_function
from fs_lib import *

@print_no_NL
@no_rlvl
@struct_printer
def pp_struct_timespec64(ts, rlvl, ilvl):
	str = timespec_to_string(ts)
	print(" - {}".format(str))


if __name__ == "__main__":
	program_display_struct(pp_struct_timespec64)

# vim: sw=4 ts=4 noexpandtab
