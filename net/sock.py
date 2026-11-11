#!/usr/bin/python

from __future__ import print_function
import socket as py_socket
import struct as py_struct
from fs_lib import *

AF_FAMILIES = {
	1: "AF_UNIX",
	2: "AF_INET",
	10: "AF_INET6",
	16: "AF_NETLINK",
	17: "AF_PACKET",
	40: "AF_VSOCK",
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

TCP_STATES = {
	1: "TCP_ESTABLISHED",
	2: "TCP_SYN_SENT",
	3: "TCP_SYN_RECV",
	4: "TCP_FIN_WAIT1",
	5: "TCP_FIN_WAIT2",
	6: "TCP_TIME_WAIT",
	7: "TCP_CLOSE",
	8: "TCP_CLOSE_WAIT",
	9: "TCP_LAST_ACK",
	10: "TCP_LISTEN",
	11: "TCP_CLOSING",
	12: "TCP_NEW_SYN_RECV",
	13: "TCP_BOUND_INACTIVE",
}

SOCK_FLAGS_C = '''
#define SOCK_DEAD 0
#define SOCK_DONE 1
#define SOCK_URGINLINE 2
#define SOCK_KEEPOPEN 3
#define SOCK_LINGER 4
#define SOCK_DESTROY 5
#define SOCK_BROADCAST 6
#define SOCK_TIMESTAMP 7
#define SOCK_ZAPPED 8
#define SOCK_USE_WRITE_QUEUE 9
#define SOCK_DBG 10
#define SOCK_RCVTSTAMP 11
#define SOCK_RCVTSTAMPNS 12
#define SOCK_LOCALROUTE 13
#define SOCK_MEMALLOC 14
#define SOCK_TIMESTAMPING_RX_SOFTWARE 15
#define SOCK_FASYNC 16
#define SOCK_RXQ_OVFL 17
#define SOCK_ZEROCOPY 18
#define SOCK_WIFI_STATUS 19
#define SOCK_NOFCS 20
#define SOCK_FILTER_LOCKED 21
#define SOCK_SELECT_ERR_QUEUE 22
#define SOCK_RCU_FREE 23
#define SOCK_TXTIME 24
#define SOCK_XDP 25
#define SOCK_TSTAMP_NEW 26
#define SOCK_RCVMARK 27
#define SOCK_RCVPRIORITY 28
#define SOCK_TIMESTAMPING_ANY 29
'''
SOCK_FLAGS = CDefine(SOCK_FLAGS_C)

SHUTDOWN_FLAGS_C = '''
#define RCV_SHUTDOWN 0
#define SEND_SHUTDOWN 1
'''
SHUTDOWN_FLAGS = CDefine(SHUTDOWN_FLAGS_C)


def format_ipv4(addr_int):
	try:
		return py_socket.inet_ntoa(py_struct.pack("=I", addr_int & 0xffffffff))
	except:
		return "0x{:08x}".format(addr_int)


def format_ipv6(in6_addr):
	try:
		raw_bytes = bytes(bytearray([int(b) for b in in6_addr.in6_u.u6_addr8]))
		return py_socket.inet_ntop(py_socket.AF_INET6, raw_bytes)
	except:
		return "<ipv6>"


@struct_label_string(("__sk_common.skc_prot.name", "sk_prot.name"))
@struct_printer
def pp_struct_sock(sk, rlvl, ilvl):
	skc = sk.__sk_common if sk.hasField("__sk_common") else sk

	fam = None
	if skc.hasField("skc_family"):
		try:
			fam = int(skc.skc_family)
			fam_name = AF_FAMILIES.get(fam, "UNKNOWN")
			print("{}.sk_family = {} ({})".format(indent_str(ilvl), fam, fam_name))
		except:
			pass

	if sk.hasField("sk_type"):
		try:
			t = int(sk.sk_type)
			t_base = t & 0xf
			t_name = SOCK_TYPES.get(t_base, "UNKNOWN")
			extra = ""
			if t & 0o2000000:
				extra += "|SOCK_NONBLOCK"
			if t & 0o20000000:
				extra += "|SOCK_CLOEXEC"
			print("{}.sk_type = {} ({}{})".format(indent_str(ilvl), t, t_name, extra))
		except:
			pass

	if sk.hasField("sk_protocol") and sk.sk_protocol:
		try:
			print("{}.sk_protocol = {}".format(indent_str(ilvl), int(sk.sk_protocol)))
		except:
			pass

	if skc.hasField("skc_state"):
		try:
			st = int(skc.skc_state)
			st_name = TCP_STATES.get(st, "UNKNOWN")
			print("{}.sk_state = {} ({})".format(indent_str(ilvl), st, st_name))
		except:
			pass

	# Addresses and ports
	if fam == 2:  # AF_INET
		try:
			saddr = int(skc.skc_rcv_saddr)
			daddr = int(skc.skc_daddr)
			sport = int(skc.skc_num)
			dport = py_socket.ntohs(int(skc.skc_dport))
			print("{}.local = {}:{}".format(indent_str(ilvl), format_ipv4(saddr), sport))
			print("{}.remote = {}:{}".format(indent_str(ilvl), format_ipv4(daddr), dport))
		except:
			pass
	elif fam == 10:  # AF_INET6
		try:
			sport = int(skc.skc_num)
			dport = py_socket.ntohs(int(skc.skc_dport))
			print("{}.local = [{}]:{}".format(indent_str(ilvl), format_ipv6(skc.skc_v6_rcv_saddr), sport))
			print("{}.remote = [{}]:{}".format(indent_str(ilvl), format_ipv6(skc.skc_v6_daddr), dport))
		except:
			pass

	if skc.hasField("skc_bound_dev_if") and skc.skc_bound_dev_if:
		try:
			print("{}.sk_bound_dev_if = {}".format(indent_str(ilvl), int(skc.skc_bound_dev_if)))
		except:
			pass

	if skc.hasField("skc_flags") and skc.skc_flags:
		try:
			fl = int(skc.skc_flags)
			fl_str = flags_to_string(fl, SOCK_FLAGS)
			print("{}.sk_flags = 0x{:x} - {}".format(indent_str(ilvl), fl, fl_str))
		except:
			pass

	if sk.hasField("sk_shutdown") and sk.sk_shutdown:
		try:
			shut = int(sk.sk_shutdown)
			shut_str = flags_to_string(shut, SHUTDOWN_FLAGS)
			print("{}.sk_shutdown = {} ({})".format(indent_str(ilvl), shut, shut_str))
		except:
			pass

	# Memory buffers
	if sk.hasField("sk_rcvbuf"):
		try:
			rcvbuf = int(sk.sk_rcvbuf)
			print("{}.sk_rcvbuf = {} ({})".format(indent_str(ilvl), rcvbuf, val_to_units_string(rcvbuf, 1024)))
		except:
			pass

	if sk.hasField("sk_sndbuf"):
		try:
			sndbuf = int(sk.sk_sndbuf)
			print("{}.sk_sndbuf = {} ({})".format(indent_str(ilvl), sndbuf, val_to_units_string(sndbuf, 1024)))
		except:
			pass

	if sk.hasField("sk_wmem_queued"):
		try:
			wmem = int(sk.sk_wmem_queued)
			print("{}.sk_wmem_queued = {} ({})".format(indent_str(ilvl), wmem, val_to_units_string(wmem, 1024)))
		except:
			pass

	# Queues
	if sk.hasField("sk_receive_queue") and sk.sk_receive_queue.hasField("qlen"):
		try:
			print("{}.sk_receive_queue.qlen = {}".format(indent_str(ilvl), int(sk.sk_receive_queue.qlen)))
		except:
			pass

	if sk.hasField("sk_write_queue") and sk.sk_write_queue.hasField("qlen"):
		try:
			print("{}.sk_write_queue.qlen = {}".format(indent_str(ilvl), int(sk.sk_write_queue.qlen)))
		except:
			pass

	if sk.hasField("sk_error_queue") and sk.sk_error_queue.hasField("qlen"):
		try:
			eqlen = int(sk.sk_error_queue.qlen)
			if eqlen > 0:
				print("{}.sk_error_queue.qlen = {}".format(indent_str(ilvl), eqlen))
		except:
			pass

	if sk.hasField("sk_drops") and sk.sk_drops.hasField("counter"):
		try:
			drops = int(sk.sk_drops.counter)
			if drops > 0:
				print("{}.sk_drops = {}".format(indent_str(ilvl), drops))
		except:
			pass

	# Callbacks
	for cb_name in ("sk_state_change", "sk_data_ready", "sk_write_space", "sk_error_report", "sk_destruct"):
		if sk.hasField(cb_name):
			try:
				cb_val = long(getattr(sk, cb_name))
				if cb_val and not is_err_or_null(cb_val):
					sym = addr2sym(cb_val)
					sym_str = " <{}>".format(sym) if sym else ""
					print("{}.{} = 0x{:x}{}".format(indent_str(ilvl), cb_name, cb_val, sym_str))
			except:
				pass

	# User data
	if sk.hasField("sk_user_data") and sk.sk_user_data and not is_err_or_null(sk.sk_user_data):
		try:
			ud_val = long(sk.sk_user_data)
			sym = addr2sym(ud_val)
			sym_str = " <{}>".format(sym) if sym else ""
			print("{}.sk_user_data = 0x{:x}{}".format(indent_str(ilvl), ud_val, sym_str))
		except:
			pass

	# Sub-structures
	if sk.hasField("sk_socket") and sk.sk_socket and not is_err_or_null(sk.sk_socket):
		pp_struct_member(sk, "sk_socket", rlvl=rlvl, ilvl=ilvl)


if __name__ == "__main__":
	program_display_struct(pp_struct_sock)

# vim: sw=4 ts=4 noexpandtab
