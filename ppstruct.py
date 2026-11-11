#!/usr/bin/python

from __future__ import print_function


import sys, os

if __name__ == "__main__":
	mypath = os.path.dirname(os.path.realpath(sys.argv[0]))
	check_paths = [mypath]
	for p in check_paths:
		if os.path.isdir(p):
			if p not in sys.path:
				sys.path.append(p)

from fs_lib import *

ppstruct_help = '''
Recursively pretty-print known structures

-r, --recurse
	increase the number of levels of recursion to display by 1 (default is {def_rlvl})
		(may be give more than once)

-c, --counts
	include structure use counts (usually suppressed)
		NOT IMPLEMENTED YET

-l, --locks
	include structure locks, mutexes, semaphores, etc. (usually suppressed)
		NOT IMPLEMENTED YET

-s, --stats
	include statistics (such as network tx/rx counts, etc.)
		NOT IMPLEMENTED YET

-n, --noprune
	do not attempt to suppress display of duplicate struct/address pairs
		usually if a (struct type, address) pair has beeen pretty-printed
		with a particular recursion level, further pretty-printing of the
		same pair which provides no additional depth of information will
		be suppressed.  This option disables this check, and redundant
		information may be displayed

		This feature is a work-in-progress
'''.format(def_rlvl=DEFAULT_RLVL)
def pp_struct__check_registerred():
	try:
		from crash import get_epython_cmds
		cmds = get_epython_cmds()
		if 'ppstruct' in cmds:
			return True
		return False
	except:
		return False

def pp_struct__register():
	try:
		from crash import register_epython_prog
		register_epython_prog("ppstruct",
				"pretty-print structures, recursively",
				"-h - list available options",
				ppstruct_help)
	except Exception as err:
		print("an error occurred while registerring the 'ppstruct' command: {e}".format(e=str(err)))

def pp_struct__parse_cmdline():
	import argparse

#	opts_parser = argparse.ArgumentParser(version='0.01')
	opts_parser = argparse.ArgumentParser()
	opts_parser.add_argument('--recurse', '-r', default=DEFAULT_RLVL, action='count')
	opts_parser.add_argument('--counts', '-c', default=False, action='store_true')
	opts_parser.add_argument('--locks', '-l', default=False, action='store_true')
	opts_parser.add_argument('--stats', '-s', default=False, action='store_true')
	opts_parser.add_argument('--noprune', '-n', dest='prune', default=True, action='store_false')

	pos_parser = argparse.ArgumentParser()
#	pos_parser.add_argument('struct_type', action='store', nargs='1')
	pos_parser.add_argument('struct_type', action='store')
	pos_parser.add_argument('addrs', action='store', nargs='*')

	kw = { 'opts': opts_parser, 'pos': pos_parser }

	def parse_cmdline(*args, **kwargs):
		opts_parser = kwargs['opts']
		pos_parser = kwargs['pos']
		ns, remain = opts_parser.parse_known_args( *args )
		ns = pos_parser.parse_args(remain, ns)
		return ns

	cmd_opts = parse_cmdline(sys.argv[1:], **kw)
	print("{}".format(cmd_opts))
	return cmd_opts

def pp_struct_cmd():
	global ppstruct_vars

	cmd_opts = pp_struct__parse_cmdline()
	if ppstruct_func_exists(cmd_opts.struct_type):
		ppstruct_vars['pp_struct_opts'] = cmd_opts

		ppstruct_vars['pp_struct_prune'] = {}
		ppstruct_vars['pp_struct_prune']['list'] = {}

		for addr_str in cmd_opts.addrs:
			addr = get_arg_value(addr_str)
			if addr:
				pp_struct(cmd_opts.struct_type, addr, rlvl=cmd_opts.recurse, ilvl=0)
		print("ppstruct_prune2: {}".format(ppstruct_vars['pp_struct_prune']))
	else:
		print("Unable to ppstruct '{type}'".format(type=cmd_opts.struct_type))

if __name__ == "__main__":
	if not pp_struct__check_registerred():
		pp_struct__register()
		if not pp_struct__check_registerred():
			print("Unable to register 'ppstruct' command")
	pp_struct_cmd()

# vim: sw=4 ts=4 noexpandtab
