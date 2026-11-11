#!/usr/bin/python

from fs_lib import *


@struct_printer
def pp_struct___wait_queue_head(wqh, rlvl, ilvl):
	pp_struct_member(wqh, "lock", rlvl=rlvl, ilvl=ilvl)
	tasklist_head = wqh.task_list

#	tmp_tl = readListByHead(tasklist_head)
	print("{}task_list head is 0x{:016x}".format(indent_str(ilvl), tasklist_head, ListHead(tasklist_head)))



if __name__ == "__main__":
	program_display_struct(pp_struct___wait_queue_head)


# vim: sw=4 ts=4 noexpandtab
