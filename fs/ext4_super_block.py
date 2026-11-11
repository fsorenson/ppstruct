#!/usr/bin/python
from __future__ import print_function

from fs_lib import *


@struct_printer
def pp_struct_ext4_super_block(es, rlvl, ilvl):
	es = readSU("struct ext4_super_block", es)

	print("{}.s_blocks_count_lo: {}".format(indent_str(ilvl), es.s_blocks_count_lo))
	print("{}.s_r_blocks_count_lo: {}".format(indent_str(ilvl), es.s_r_blocks_count_lo))
	print("{}.s_free_blocks_count_lo: {}".format(indent_str(ilvl), es.s_free_blocks_count_lo))

if __name__ == "__main__":
	program_display_struct(pp_struct_ext4_super_block)

# vim: sw=4 ts=4 noexpandtab
