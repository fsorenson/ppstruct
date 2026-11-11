#!/usr/bin/python

from __future__ import print_function
from fs_lib import *

@struct_printer
def pp_struct_tcon_link(tl, rlvl, ilvl):
	if tl.hasField("tl_uid"):
		try:
			print("{}.tl_uid: {}".format(indent_str(ilvl), tl.tl_uid.val))
		except:
			pass

	if tl.hasField("tl_count"):
		try:
			print("{}.tl_count: {}".format(indent_str(ilvl), int(tl.tl_count.counter)))
		except:
			pass

	if tl.hasField("tl_flags"):
		print("{}.tl_flags: 0x{:x}".format(indent_str(ilvl), int(tl.tl_flags)))

	if tl.hasField("tl_tcon") and tl.tl_tcon and long(tl.tl_tcon) != 0:
		pp_struct_member(tl, "tl_tcon", rlvl=rlvl, ilvl=ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_tcon_link)

# vim: sw=4 ts=4 noexpandtab
