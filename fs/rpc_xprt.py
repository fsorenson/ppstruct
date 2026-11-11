#!/usr/bin/python

from __future__ import print_function
from fs_lib import *

XPRT_STATE_FLAGS_C = '''
#define XPRT_LOCKED         0
#define XPRT_CONNECTED      1
#define XPRT_CONNECTING     2
#define XPRT_CLOSE_WAIT     3
#define XPRT_BOUND          4
#define XPRT_BINDING        5
#define XPRT_CLOSING        6
#define XPRT_OFFLINE        7
#define XPRT_REMOVE         8
#define XPRT_CONGESTED      9
#define XPRT_CWND_WAIT      10
#define XPRT_WRITE_SPACE    11
#define XPRT_SND_IS_COOKIE  12
'''
XPRT_STATE_FLAGS = CDefine(XPRT_STATE_FLAGS_C)

PROTO_MAP = {
	6: "tcp",
	17: "udp",
	262: "rdma",
}

@struct_label_string(("servername", "address_strings[0]"))
@struct_printer
def pp_struct_rpc_xprt(xprt, rlvl, ilvl):

	if xprt.hasField("servername") and xprt.servername and not is_err_or_null(xprt.servername):
		try:
			print("{}.servername = '{}'".format(indent_str(ilvl), xprt.servername))
		except:
			pass

	if xprt.hasField("addr"):
		try:
			peer_str = decode_sockaddr_storage(xprt.addr)
			if peer_str:
				print("{}.addr = '{}'".format(indent_str(ilvl), peer_str))
		except:
			pass

	if xprt.hasField("xprt_class") and xprt.xprt_class and not is_err_or_null(xprt.xprt_class):
		try:
			print("{}.xprt_class = '{}'".format(indent_str(ilvl), xprt.xprt_class.name))
		except:
			pass

	if xprt.hasField("prot"):
		try:
			p = int(xprt.prot)
			p_name = PROTO_MAP.get(p, "unknown")
			print("{}.prot = {} ({})".format(indent_str(ilvl), p, p_name))
		except:
			pass

	flags = []
	if xprt.hasField("main") and xprt.main:
		flags.append("main")
	if xprt.hasField("resvport") and xprt.resvport:
		flags.append("resvport")
	if xprt.hasField("reuseport") and xprt.reuseport:
		flags.append("reuseport")
	if flags:
		print("{}.flags = {}".format(indent_str(ilvl), ", ".join(flags)))

	if xprt.hasField("state"):
		try:
			st = int(xprt.state)
			st_str = flags_to_string(st, XPRT_STATE_FLAGS)
			print("{}.state = 0x{:x} - {}".format(indent_str(ilvl), st, st_str))
		except:
			pass

	if xprt.hasField("cwnd"):
		try:
			cong = int(xprt.cong) if xprt.hasField("cong") else 0
			cwnd = int(xprt.cwnd)
			print("{}.cong/cwnd = {}/{}".format(indent_str(ilvl), cong, cwnd))
		except:
			pass

	if xprt.hasField("max_payload") and xprt.max_payload:
		try:
			mp = int(xprt.max_payload)
			print("{}.max_payload = {} ({})".format(indent_str(ilvl), mp, val_to_units_string(mp, 1024)))
		except:
			pass

	if xprt.hasField("num_reqs"):
		try:
			n_reqs = int(xprt.num_reqs)
			min_r = int(xprt.min_reqs) if xprt.hasField("min_reqs") else 0
			max_r = int(xprt.max_reqs) if xprt.hasField("max_reqs") else 0
			print("{}.reqs = {} (min: {}, max: {})".format(indent_str(ilvl), n_reqs, min_r, max_r))
		except:
			pass

	if xprt.hasField("queuelen"):
		try:
			qlen = int(xprt.queuelen.counter)
			xmit_qlen = int(xprt.xmit_queuelen.counter) if xprt.hasField("xmit_queuelen") else 0
			print("{}.queuelen = {} (xmit: {})".format(indent_str(ilvl), qlen, xmit_qlen))
		except:
			pass

	if xprt.hasField("stat"):
		try:
			st = xprt.stat
			sends = int(st.sends)
			recvs = int(st.recvs)
			bad_xids = int(st.bad_xids)
			connect_count = int(st.connect_count)
			max_slots = int(st.max_slots)
			print("{}.stat: sends={}, recvs={}, bad_xids={}, connects={}, max_slots={}".format(
				indent_str(ilvl), sends, recvs, bad_xids, connect_count, max_slots))
		except:
			pass

	# Timeout
	if xprt.hasField("timeout") and not is_err_or_null(xprt.timeout):
		pp_struct_member(xprt, "timeout", rlvl=rlvl, ilvl=ilvl)

	# Socket-specific info if struct sock_xprt
	is_sock = False
	try:
		if xprt.hasField("xprt_class") and xprt.xprt_class:
			cls_name = xprt.xprt_class.name
			if cls_name in ["tcp", "udp", "tcp-tls"]:
				is_sock = True
	except:
		pass

	if is_sock:
		try:
			sx = readSU("struct sock_xprt", long(xprt))
			if sx.hasField("srcaddr"):
				src_str = decode_sockaddr_storage(sx.srcaddr)
				if src_str and not src_str.startswith("0.0.0.0") and not src_str.startswith("::"):
					print("{}.srcaddr = '{}'".format(indent_str(ilvl), src_str))
			if sx.hasField("sock") and not is_err_or_null(sx.sock):
				pp_struct_member(sx, "sock", rlvl=rlvl, ilvl=ilvl)
			if sx.hasField("file") and not is_err_or_null(sx.file):
				pp_struct_member(sx, "file", rlvl=rlvl, ilvl=ilvl)
		except:
			pass

	# Net namespace
	if xprt.hasField("xprt_net") and not is_err_or_null(xprt.xprt_net):
		pp_struct_member(xprt, "xprt_net", rlvl=rlvl, ilvl=ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_rpc_xprt)

# vim: sw=4 ts=4 noexpandtab
