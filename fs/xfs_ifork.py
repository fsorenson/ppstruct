#!/usr/bin/python
from fs_lib import *

XFS_DINODE_FMT_NAMES = {
	0: "DEV",
	1: "LOCAL",
	2: "EXTENTS",
	3: "BTREE",
	4: "UUID",
	5: "RMAP",
}

@struct_printer
def pp_struct_xfs_ifork(ifork, rlvl, ilvl):
	fmt_str = ""
	if ifork.hasField("if_format"):
		fmt_val = int(ifork.if_format)
		fmt_name = XFS_DINODE_FMT_NAMES.get(fmt_val, "UNKNOWN")
		fmt_str = ".if_format = {} ({})".format(fmt_val, fmt_name)

	parts = []
	if fmt_str:
		parts.append(fmt_str)
	if ifork.hasField("if_bytes"):
		parts.append(".if_bytes = {}".format(int(ifork.if_bytes)))
	if ifork.hasField("if_nextents"):
		parts.append(".if_nextents = {}".format(int(ifork.if_nextents)))
	if ifork.hasField("if_height") and int(ifork.if_height) > 0:
		parts.append(".if_height = {}".format(int(ifork.if_height)))

	if parts:
		print(indent_str(ilvl) + ", ".join(parts))

	if ifork.hasField("if_broot") and long(ifork.if_broot) != 0:
		pp_struct_member(ifork, "if_broot", rlvl=rlvl, ilvl=ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_xfs_ifork)
