#!/usr/bin/python

from __future__ import print_function
from fs_lib import *

@struct_label_string("charset")
@struct_printer
def pp_struct_nls_table(nls, rlvl, ilvl):
	if nls.hasField("alias") and nls.alias and long(nls.alias) != 0:
		try:
			print("{}.alias: '{}'".format(indent_str(ilvl), nls.alias))
		except:
			pass

if __name__ == "__main__":
	program_display_struct(pp_struct_nls_table)

# vim: sw=4 ts=4 noexpandtab
