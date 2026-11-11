#!/usr/bin/python

from __future__ import print_function
from fs_lib import *

@struct_label_string("tree_name")
@struct_printer
def pp_struct_cifs_tcon(tcon, rlvl, ilvl):
	if tcon.hasField("tid"):
		print("{}.tid: {}".format(indent_str(ilvl), tcon.tid))

	if tcon.hasField("status"):
		print("{}.status: {}".format(indent_str(ilvl), tcon.status))

	if tcon.hasField("num_local_opens") and tcon.hasField("num_remote_opens"):
		try:
			print("{}.opens: local = {}, remote = {}".format(
				indent_str(ilvl), int(tcon.num_local_opens.counter), int(tcon.num_remote_opens.counter)))
		except:
			pass

	if tcon.hasField("bytes_read") and tcon.hasField("bytes_written"):
		bread = int(tcon.bytes_read)
		bwritten = int(tcon.bytes_written)
		print("{}.bytes: read = {} ({}), written = {} ({})".format(
			indent_str(ilvl),
			bread, val_to_units_string(bread, 1024),
			bwritten, val_to_units_string(bwritten, 1024)))

if __name__ == "__main__":
	program_display_struct(pp_struct_cifs_tcon)

# vim: sw=4 ts=4 noexpandtab
