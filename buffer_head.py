#!/usr/bin/python

from __future__ import print_function

from fs_lib import *


@struct_printer
def pp_struct_buffer_head(bh, rlvl, ilvl):

	print("{}.b_blocknr = {bnum}, .b_size = {b_size}".format(indent_str(ilvl), bnum=bh.b_blocknr, b_size=bh.b_size))
	b_state = bh.b_state

	b_state_strings = []
	for bit in range(0, member_size("struct buffer_head", "b_state") * 4 - 1):
		if (b_state & (1 << bit)):
			b_state_strings.append(get_enum_string(bit, "bh_state_bits"))

	b_state_string = "|".join(str(s) for s in b_state_strings)
	print("{}.b_state = {}".format(indent_str(ilvl), b_state_string))

	pp_struct_member(bh, "b_page", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(bh, "b_bdev", rlvl=rlvl, ilvl=ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_buffer_head)

# vim: sw=4 ts=4 noexpandtab
