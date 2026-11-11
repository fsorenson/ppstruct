#!/usr/bin/python

from __future__ import print_function
from fs_lib import *


@struct_label_string(("ns.inum",))
@struct_printer
def pp_struct_net(net, rlvl, ilvl):

	if net.hasField("ns") and net.ns.hasField("inum"):
		try:
			inum = int(net.ns.inum)
			print("{}.ns.inum = {} (net:[{}])".format(indent_str(ilvl), inum, inum))
		except:
			pass

	if net.hasField("net_cookie"):
		try:
			print("{}.net_cookie = {}".format(indent_str(ilvl), int(net.net_cookie)))
		except:
			pass

	if net.hasField("passive"):
		try:
			ref = int(net.passive.refs.counter)
			print("{}.passive = {}".format(indent_str(ilvl), ref))
		except:
			pass

	if net.hasField("ifindex"):
		try:
			print("{}.ifindex = {}".format(indent_str(ilvl), int(net.ifindex)))
		except:
			pass

	if net.hasField("is_dying") and net.is_dying:
		try:
			print("{}.is_dying = {}".format(indent_str(ilvl), bool(net.is_dying)))
		except:
			pass

	if net.hasField("user_ns") and not is_err_or_null(net.user_ns):
		try:
			u_addr = long(net.user_ns)
			u_sym = addr2sym(u_addr)
			u_sym_str = " <{}>".format(u_sym) if u_sym else ""
			print("{}.user_ns(struct user_namespace *)0x{:x}{}".format(indent_str(ilvl), u_addr, u_sym_str))
		except:
			pass

	if net.hasField("loopback_dev") and not is_err_or_null(net.loopback_dev):
		try:
			lo_addr = long(net.loopback_dev)
			lo_name = str(net.loopback_dev.name)
			print("{}.loopback_dev = {} (struct net_device *)0x{:x}".format(indent_str(ilvl), lo_name, lo_addr))
		except:
			pass

	if net.hasField("dev_base_head"):
		try:
			devs = readSUListFromHead(Addr(net.dev_base_head), "dev_list", "struct net_device")
			print("{}.dev_base_head ({} devices):".format(indent_str(ilvl), len(devs)))
			for dev in devs:
				dev_name = str(dev.name)
				dev_if = int(dev.ifindex) if dev.hasField("ifindex") else 0
				print("{}{}: {} (struct net_device *)0x{:x}".format(indent_str(ilvl + 1), dev_if, dev_name, long(dev)))
		except:
			pass

	if net.hasField("rtnl") and not is_err_or_null(net.rtnl):
		try:
			print("{}.rtnl = (struct sock *)0x{:x}".format(indent_str(ilvl), long(net.rtnl)))
		except:
			pass

	if net.hasField("genl_sock") and not is_err_or_null(net.genl_sock):
		try:
			print("{}.genl_sock = (struct sock *)0x{:x}".format(indent_str(ilvl), long(net.genl_sock)))
		except:
			pass

	if net.hasField("proc_net") and not is_err_or_null(net.proc_net):
		try:
			print("{}.proc_net = (struct proc_dir_entry *)0x{:x}".format(indent_str(ilvl), long(net.proc_net)))
		except:
			pass


if __name__ == "__main__":
	program_display_struct(pp_struct_net)

# vim: sw=4 ts=4 noexpandtab
