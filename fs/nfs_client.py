#!/usr/bin/python

from __future__ import print_function
from fs_lib import *

NFS_CS_FLAGS_C = '''
#define NFS_CS_NORESVPORT         0
#define NFS_CS_DISCRTRY           1
#define NFS_CS_MIGRATION          2
#define NFS_CS_INFINITE_SLOTS     3
#define NFS_CS_NO_RETRANS_TIMEOUT 4
#define NFS_CS_TSM_POSSIBLE       5
#define NFS_CS_NOPING             6
#define NFS_CS_DS                 7
#define NFS_CS_REUSEPORT          8
#define NFS_CS_PNFS               9
#define NFS_CS_NETUNREACH_FATAL   10
'''
NFS_CS_FLAGS = CDefine(NFS_CS_FLAGS_C)

NFS_CS_RES_FLAGS_C = '''
#define NFS_CS_CALLBACK           1
#define NFS_CS_IDMAP              2
#define NFS_CS_RENEWD             3
#define NFS_CS_STOP_RENEW         4
#define NFS_CS_CHECK_LEASE_TIME   5
'''
NFS_CS_RES_FLAGS = CDefine(NFS_CS_RES_FLAGS_C)

NFS4_CLNT_STATE_FLAGS_C = '''
#define NFS4CLNT_MANAGER_RUNNING        0
#define NFS4CLNT_CHECK_LEASE            1
#define NFS4CLNT_LEASE_EXPIRED          2
#define NFS4CLNT_RECLAIM_REBOOT         3
#define NFS4CLNT_RECLAIM_NOGRACE        4
#define NFS4CLNT_DELEGRETURN            5
#define NFS4CLNT_SESSION_RESET          6
#define NFS4CLNT_LEASE_CONFIRM          7
#define NFS4CLNT_SERVER_SCOPE_MISMATCH  8
#define NFS4CLNT_PURGE_STATE            9
#define NFS4CLNT_BIND_CONN_TO_SESSION   10
#define NFS4CLNT_MOVED                  11
#define NFS4CLNT_LEASE_MOVED            12
#define NFS4CLNT_DELEGATION_EXPIRED     13
#define NFS4CLNT_RUN_MANAGER            14
#define NFS4CLNT_MANAGER_AVAILABLE      15
#define NFS4CLNT_RECALL_RUNNING         16
#define NFS4CLNT_RECALL_ANY_LAYOUT_READ 17
#define NFS4CLNT_RECALL_ANY_LAYOUT_RW   18
#define NFS4CLNT_DELEGRETURN_DELAYED    19
'''
NFS4_CLNT_STATE_FLAGS = CDefine(NFS4_CLNT_STATE_FLAGS_C)

CONS_STATE_MAP = {
	0: "READY",
	1: "INITING",
	2: "SESSION_INITING",
}

PROTO_MAP = {
	6: "tcp",
	17: "udp",
	262: "rdma",
}

@struct_label_string(("cl_hostname", "cl_owner_id"))
@struct_printer
def pp_struct_nfs_client(clp, rlvl, ilvl):

	if clp.hasField("cl_hostname") and clp.cl_hostname and not is_err_or_null(clp.cl_hostname):
		try:
			print("{}.cl_hostname = '{}'".format(indent_str(ilvl), clp.cl_hostname))
		except:
			pass

	if clp.hasField("cl_addr"):
		try:
			addr_str = decode_sockaddr_storage(clp.cl_addr)
			if addr_str:
				print("{}.cl_addr = '{}'".format(indent_str(ilvl), addr_str))
		except:
			pass

	if clp.hasField("cl_ipaddr") and clp.cl_ipaddr:
		try:
			print("{}.cl_ipaddr = '{}'".format(indent_str(ilvl), clp.cl_ipaddr))
		except:
			pass

	if clp.hasField("cl_proto"):
		try:
			proto = int(clp.cl_proto)
			proto_name = PROTO_MAP.get(proto, "unknown")
			print("{}.cl_proto = {} ({})".format(indent_str(ilvl), proto, proto_name))
		except:
			pass

	if clp.hasField("cl_minorversion"):
		try:
			mv = int(clp.cl_minorversion)
			print("{}.version = NFSv4.{}".format(indent_str(ilvl), mv))
		except:
			pass

	if clp.hasField("cl_clientid"):
		try:
			cid = int(clp.cl_clientid)
			print("{}.cl_clientid = 0x{:016x} ({})".format(indent_str(ilvl), cid, cid))
		except:
			pass

	if clp.hasField("cl_owner_id") and clp.cl_owner_id and not is_err_or_null(clp.cl_owner_id):
		try:
			print("{}.cl_owner_id = '{}'".format(indent_str(ilvl), clp.cl_owner_id))
		except:
			pass

	if clp.hasField("cl_principal") and clp.cl_principal and not is_err_or_null(clp.cl_principal):
		try:
			print("{}.cl_principal = '{}'".format(indent_str(ilvl), clp.cl_principal))
		except:
			pass

	if clp.hasField("cl_cons_state"):
		try:
			cs = int(clp.cl_cons_state)
			cs_str = CONS_STATE_MAP.get(cs, "UNKNOWN" if cs >= 0 else "ERROR ({})".format(cs))
			print("{}.cl_cons_state = {} ({})".format(indent_str(ilvl), cs, cs_str))
		except:
			pass

	if clp.hasField("cl_flags") and clp.cl_flags:
		try:
			fl = int(clp.cl_flags)
			fl_str = flags_to_string(fl, NFS_CS_FLAGS)
			print("{}.cl_flags = 0x{:x} - {}".format(indent_str(ilvl), fl, fl_str))
		except:
			pass

	if clp.hasField("cl_res_state") and clp.cl_res_state:
		try:
			rs = int(clp.cl_res_state)
			rs_str = flags_to_string(rs, NFS_CS_RES_FLAGS)
			print("{}.cl_res_state = 0x{:x} - {}".format(indent_str(ilvl), rs, rs_str))
		except:
			pass

	if clp.hasField("cl_state") and clp.cl_state:
		try:
			st = int(clp.cl_state)
			st_str = flags_to_string(st, NFS4_CLNT_STATE_FLAGS)
			print("{}.cl_state = 0x{:x} - {}".format(indent_str(ilvl), st, st_str))
		except:
			pass

	if clp.hasField("cl_lease_time") and clp.cl_lease_time:
		try:
			lt = int(clp.cl_lease_time)
			print("{}.cl_lease_time = {} ({}s)".format(indent_str(ilvl), lt, lt // 1000))
		except:
			pass

	if clp.hasField("cl_nconnect") and clp.hasField("cl_max_connect"):
		try:
			print("{}.cl_nconnect = {} (max: {})".format(indent_str(ilvl), int(clp.cl_nconnect), int(clp.cl_max_connect)))
		except:
			pass

	if clp.hasField("cl_count"):
		try:
			cnt = int(clp.cl_count.refs.counter) if hasattr(clp.cl_count, 'refs') else int(clp.cl_count)
			print("{}.cl_count = {}".format(indent_str(ilvl), cnt))
		except:
			pass

	# Sub-structures
	if clp.hasField("cl_rpcclient") and not is_err_or_null(clp.cl_rpcclient):
		pp_struct_member(clp, "cl_rpcclient", rlvl=rlvl, ilvl=ilvl)

	if clp.hasField("cl_session") and not is_err_or_null(clp.cl_session):
		pp_struct_member(clp, "cl_session", rlvl=rlvl, ilvl=ilvl)

	if clp.hasField("cl_net") and not is_err_or_null(clp.cl_net):
		pp_struct_member(clp, "cl_net", rlvl=rlvl, ilvl=ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_nfs_client)

# vim: sw=4 ts=4 noexpandtab
