#!/usr/bin/python

from __future__ import print_function

from fs_lib import *

@print_oneline
@no_rlvl
@struct_printer
def pp_struct_rpc_timeout(to, rlvl, ilvl):
	to = readSU("struct rpc_timeout", to)

	print("{}.to_initval = {} ({} sec), .to_retries = {}".format(indent_str(ilvl), to.to_initval, to.to_initval/1000, to.to_retries))

# vim: sw=4 ts=4 noexpandtab
