#!/usr/bin/python
from pykdump.API import *
from LinuxDump.Tasks import TaskTable





def page_address(page_addr):
	ret = exec_crash_command("kmem 0x%016x" % page_addr)
	ret2 = ()
	for l in ret.split("\n"):
		if "ffff" in l:
			phys = l.split()[1]
			ret2 = exec_crash_command("ptov 0x%s" % phys)
	for l in ret2.split("\n"):
		if "ffff" in l:
			return int(l.split()[0], 16)
	return 0


# vim: sw=4 ts=4 noexpandtab
