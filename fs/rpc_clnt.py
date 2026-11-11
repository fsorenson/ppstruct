#!/usr/bin/python

from __future__ import print_function

from fs_lib import *


@struct_printer
def pp_struct_rpc_clnt(rpc_clnt, rlvl, ilvl):
	rpc_clnt = readSU("struct rpc_clnt", rpc_clnt)

	protname = ""
	try:
		protname = ", .protname = '{}'".format(rpc_clnt.cl_protname)
	except:
		pass

	print("{}.cl_vers = {}{}".format(indent_str(ilvl), rpc_clnt.cl_vers, protname))
	pp_struct_member(rpc_clnt, "cl_server", rlvl=rlvl, ilvl=ilvl)
	# could put in output for rpc_stat from clnt->cl_stats, and rpc_iostats from clnt->cl_metrics

	print("{}.cl_nodename = '{}'".format(indent_str(ilvl), rpc_clnt.cl_nodename))

	pp_struct_member(rpc_clnt, "cl_timeout", rlvl=rlvl, ilvl=ilvl)

	pp_struct_member(rpc_clnt, "cl_xprt", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(rpc_clnt, "cl_auth", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(rpc_clnt, "cl_parent", rlvl=rlvl, ilvl=ilvl)

	if rpc_clnt.hasField("cl_tasks"):
		try:
			tasks = readSUListFromHead(Addr(rpc_clnt.cl_tasks), "tk_task", "struct rpc_task")
			if tasks:
				print("{}.cl_tasks ({} tasks):".format(indent_str(ilvl), len(tasks)))
				for t in tasks:
					print("{}".format(indent_str(ilvl + 1)), end="")
					pp_struct("rpc_task", long(t), rlvl=rlvl, ilvl=ilvl + 1)
			else:
				print("{}.cl_tasks = empty".format(indent_str(ilvl)))
		except:
			pass


if __name__ == "__main__":
	program_display_struct(pp_struct_rpc_clnt)

# vim: sw=4 ts=4 noexpandtab
