#!/usr/bin/python

from __future__ import print_function

from fs_lib import *

@print_oneline
@no_rlvl
@struct_printer
def pp_struct_rpc_timeout(to, rlvl, ilvl):
	to = readSU("struct rpc_timeout", to)

	items = []
	if to.hasField("to_initval"):
		items.append(".to_initval = {} ({} sec)".format(to.to_initval, float(to.to_initval) / 1000))
	if to.hasField("to_retries"):
		items.append(".to_retries = {}".format(to.to_retries))
	if to.hasField("to_maxval") and to.hasField("to_initval") and to.to_maxval != to.to_initval:
		items.append(".to_maxval = {} ({} sec)".format(to.to_maxval, float(to.to_maxval) / 1000))

	if items:
		print(" - {}".format(", ".join(items)))

# vim: sw=4 ts=4 noexpandtab
