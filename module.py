#!/usr/bin/python

from fs_lib import *

MOD_STATE = {0: 'LIVE', 1: 'COMING', 2: 'GOING', 3: 'UNFORMED'}

@struct_printer
def pp_struct_module(module, rlvl, ilvl):

	print("{}.name = '{}'".format(indent_str(ilvl), module.name))
	if module.hasField("state"):
		st = MOD_STATE.get(int(module.state), str(module.state))
		print("{}.state = {} ({})".format(indent_str(ilvl), module.state, st))
	if module.hasField("refcnt"):
		ref = module.refcnt.counter if hasattr(module.refcnt, 'counter') else module.refcnt
		print("{}.refcnt = {}".format(indent_str(ilvl), ref))
	if module.hasField("taints") and module.taints:
		print("{}.taints = 0x{:x}".format(indent_str(ilvl), module.taints))
	print("{}.version = '{}'".format(indent_str(ilvl), module.version))
	print("{}.srcversion = '{}'".format(indent_str(ilvl), module.srcversion))
	if module.hasField("args"):
		print("{}.args = '{}'".format(indent_str(ilvl), module.args))
	if module.hasField("num_syms"):
		print("{}.num_syms = '{}'".format(indent_str(ilvl), module.num_syms))
	if module.hasField("num_gpl_syms"):
		print("{}.num_gpl_syms = '{}'".format(indent_str(ilvl), module.num_gpl_syms))

if __name__ == "__main__":
	program_display_struct(pp_struct_module)

# vim: sw=4 ts=4 noexpandtab
