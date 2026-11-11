#!/usr/bin/python
from fs_lib import *

@struct_label_string("disk_name")
@struct_printer
def pp_struct_gendisk(gendisk, rlvl, ilvl):

	print("{}.disk_name - {}".format(indent_str(ilvl), gendisk.disk_name))

	pp_struct_member(gendisk, "queue", rlvl, ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_gendisk)

# vim: sw=4 ts=4 noexpandtab
