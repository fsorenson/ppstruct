#!/usr/bin/python

from __future__ import print_function
from fs_lib import *

SOCKET_STATES = {
	0: "SS_FREE",
	1: "SS_UNCONNECTED",
	2: "SS_CONNECTING",
	3: "SS_CONNECTED",
	4: "SS_DISCONNECTING",
}

SOCK_TYPES = {
	1: "SOCK_STREAM",
	2: "SOCK_DGRAM",
	3: "SOCK_RAW",
	4: "SOCK_RDM",
	5: "SOCK_SEQPACKET",
	6: "SOCK_DCCP",
	10: "SOCK_PACKET",
}

SOCK_FLAGS_C = '''
#define SOCKWQ_ASYNC_NOSPACE  0
#define SOCKWQ_ASYNC_WAITDATA 1
#define SOCK_NOSPACE          2
#define SOCK_SUPPORT_ZC       3
#define SOCK_CUSTOM_SOCKOPT   4
'''
SOCK_FLAGS = CDefine(SOCK_FLAGS_C)

AF_FAMILIES = {
	1: "AF_UNIX",
	2: "AF_INET",
	10: "AF_INET6",
	16: "AF_NETLINK",
	17: "AF_PACKET",
	40: "AF_VSOCK",
}

@struct_label_string(("sk.__sk_common.skc_prot.name", "file.f_path.dentry.d_name.name"))
@struct_printer
def pp_struct_socket(sock, rlvl, ilvl):

	if sock.hasField("state"):
		try:
			st = int(sock.state)
			st_name = SOCKET_STATES.get(st, "UNKNOWN")
			print("{}.state = {} ({})".format(indent_str(ilvl), st, st_name))
		except:
			pass

	if sock.hasField("type"):
		try:
			t = int(sock.type)
			t_base = t & 0xf
			t_name = SOCK_TYPES.get(t_base, "UNKNOWN")
			extra = ""
			if t & 0o2000000: # SOCK_NONBLOCK
				extra += "|SOCK_NONBLOCK"
			if t & 0o20000000: # SOCK_CLOEXEC
				extra += "|SOCK_CLOEXEC"
			print("{}.type = {} ({}{})".format(indent_str(ilvl), t, t_name, extra))
		except:
			pass

	if sock.hasField("flags") and sock.flags:
		try:
			fl = int(sock.flags)
			fl_str = flags_to_string(fl, SOCK_FLAGS)
			print("{}.flags = 0x{:x} - {}".format(indent_str(ilvl), fl, fl_str))
		except:
			pass

	if sock.hasField("ops") and sock.ops and not is_err_or_null(sock.ops):
		try:
			ops_addr = long(sock.ops)
			sym = addr2sym(ops_addr)
			sym_str = " <{}>".format(sym) if sym else ""
			fam_str = ""
			if sock.ops.hasField("family"):
				fam = int(sock.ops.family)
				fam_name = AF_FAMILIES.get(fam, "UNKNOWN")
				fam_str = " (family: {} - {})".format(fam, fam_name)
			print("{}.ops(struct proto_ops *)0x{:x}{}{}".format(indent_str(ilvl), ops_addr, sym_str, fam_str))
		except:
			pass

	# Sub-structures
	if sock.hasField("file") and not is_err_or_null(sock.file):
		pp_struct_member(sock, "file", rlvl=rlvl, ilvl=ilvl)

	if sock.hasField("sk") and not is_err_or_null(sock.sk):
		pp_struct_member(sock, "sk", rlvl=rlvl, ilvl=ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_socket)

# vim: sw=4 ts=4 noexpandtab
