#!/usr/bin/python
from fs_lib import *

@struct_printer
def pp_struct_xfs_imap(imap, rlvl, ilvl):
	parts = []
	if imap.hasField("im_agbno"):
		parts.append(".im_agbno = {}".format(imap.im_agbno))
	if imap.hasField("im_blkno"):
		parts.append(".im_blkno = {}".format(imap.im_blkno))
	if imap.hasField("im_boffset"):
		parts.append(".im_boffset = {}".format(imap.im_boffset))
	if imap.hasField("im_len"):
		parts.append(".im_len = {}".format(imap.im_len))
	print(indent_str(ilvl) + ", ".join(parts))

if __name__ == "__main__":
	program_display_struct(pp_struct_xfs_imap)
