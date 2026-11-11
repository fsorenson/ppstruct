#!/usr/bin/python

from __future__ import print_function
import socket
import struct
from fs_lib import *

def decode_sockaddr_storage(ksockaddr):
	try:
		family = int(ksockaddr.ss_family)
		data = ksockaddr.__data.ByteArray
		if family == socket.AF_INET:
			port = data[0] * 256 + data[1]
			ip = socket.inet_ntop(socket.AF_INET, struct.pack('4B', *data[2:6]))
			return "{}:{}".format(ip, port) if port else ip
		elif family == socket.AF_INET6:
			port = data[0] * 256 + data[1]
			ip = socket.inet_ntop(socket.AF_INET6, struct.pack('16B', *data[6:22]))
			return "[{}]:{}".format(ip, port) if port else ip
	except Exception:
		pass
	return None

@struct_label_string(("source", "UNC"))
@struct_printer
def pp_struct_smb3_fs_context(ctx, rlvl, ilvl):
	# Source / Share / Host
	if ctx.hasField("source") and ctx.source:
		print("{}.source = '{}'".format(indent_str(ilvl), ctx.source))
	if ctx.hasField("UNC") and ctx.UNC:
		print("{}.UNC = '{}'".format(indent_str(ilvl), ctx.UNC))
	if ctx.hasField("server_hostname") and ctx.server_hostname:
		port_str = ":{}".format(ctx.port) if ctx.hasField("port") and ctx.port else ""
		print("{}.server = '{}{}'".format(indent_str(ilvl), ctx.server_hostname, port_str))

	if ctx.hasField("dstaddr"):
		dst = decode_sockaddr_storage(ctx.dstaddr)
		if dst:
			print("{}.dstaddr = {}".format(indent_str(ilvl), dst))

	# Credentials
	cred_parts = []
	if ctx.hasField("username") and ctx.username:
		cred_parts.append("user: '{}'".format(ctx.username))
	if ctx.hasField("domainname") and ctx.domainname:
		cred_parts.append("domain: '{}'".format(ctx.domainname))
	if ctx.hasField("sectype"):
		cred_parts.append("sec: {}".format(ctx.sectype))
	if cred_parts:
		print("{}.auth: {}".format(indent_str(ilvl), ", ".join(cred_parts)))

	# UID / GID
	uids = []
	if ctx.hasField("linux_uid"):
		try:
			uids.append("uid: {}".format(ctx.linux_uid.val))
		except:
			pass
	if ctx.hasField("linux_gid"):
		try:
			uids.append("gid: {}".format(ctx.linux_gid.val))
		except:
			pass
	if ctx.hasField("cred_uid"):
		try:
			if ctx.cred_uid.val != ctx.linux_uid.val:
				uids.append("cred_uid: {}".format(ctx.cred_uid.val))
		except:
			pass
	if uids:
		print("{}.ids: {}".format(indent_str(ilvl), ", ".join(uids)))

	# File / Directory permissions
	if ctx.hasField("file_mode") and ctx.hasField("dir_mode"):
		print("{}.mode: file = 0{:o}, dir = 0{:o}".format(
			indent_str(ilvl), int(ctx.file_mode), int(ctx.dir_mode)))

	# SMB Dialect / Version
	if ctx.hasField("vals") and ctx.vals and long(ctx.vals) != 0:
		try:
			print("{}.smb_version = '{}'".format(indent_str(ilvl), ctx.vals.version_string))
		except:
			pass

	# Buffer & I/O sizes
	io_sizes = []
	if ctx.hasField("rsize") and ctx.rsize:
		rsize = int(ctx.rsize)
		io_sizes.append("rsize: {} ({})".format(rsize, val_to_units_string(rsize, 1024)))
	if ctx.hasField("wsize") and ctx.wsize:
		wsize = int(ctx.wsize)
		io_sizes.append("wsize: {} ({})".format(wsize, val_to_units_string(wsize, 1024)))
	if ctx.hasField("bsize") and ctx.bsize:
		bsize = int(ctx.bsize)
		io_sizes.append("bsize: {} ({})".format(bsize, val_to_units_string(bsize, 1024)))
	if io_sizes:
		print("{}.io_sizes: {}".format(indent_str(ilvl), ", ".join(io_sizes)))

	# Active options/flags
	bool_fields = [
		'sign', 'seal', 'resilient', 'rdma', 'multichannel', 'compress', 'server_ino',
		'direct_io', 'strict_io', 'mfsymlinks', 'multiuser', 'posix_paths', 'nocase',
		'nobrl', 'fsc', 'rootfs', 'witness', 'nodfs', 'local_lease', 'nohandlecache',
		'dynperm', 'noperm', 'nodelete', 'mode_ace', 'no_psx_acl', 'cifs_acl',
		'no_xattr', 'remap', 'sfu_remap', 'sfu_emul', 'nullauth', 'mand_lock'
	]
	active_opts = []
	for bf in bool_fields:
		if ctx.hasField(bf) and getattr(ctx, bf):
			active_opts.append(bf)
	if active_opts:
		print("{}.options: {}".format(indent_str(ilvl), ", ".join(active_opts)))

	# Timeouts / parameters
	params = []
	if ctx.hasField("echo_interval") and ctx.echo_interval:
		params.append("echo_interval: {}s".format(ctx.echo_interval))
	if ctx.hasField("max_channels") and ctx.max_channels > 1:
		params.append("max_channels: {}".format(ctx.max_channels))
	if ctx.hasField("acregmax") and ctx.acregmax:
		params.append("acregmax: {}".format(ctx.acregmax))
	if ctx.hasField("acdirmax") and ctx.acdirmax:
		params.append("acdirmax: {}".format(ctx.acdirmax))
	if ctx.hasField("closetimeo") and ctx.closetimeo:
		params.append("closetimeo: {}".format(ctx.closetimeo))
	if params:
		print("{}.params: {}".format(indent_str(ilvl), ", ".join(params)))

	# NLS
	if ctx.hasField("iocharset") and ctx.iocharset:
		print("{}.iocharset: '{}'".format(indent_str(ilvl), ctx.iocharset))
	if ctx.hasField("local_nls") and ctx.local_nls and long(ctx.local_nls) != 0:
		pp_struct_member(ctx, "local_nls", rlvl=rlvl, ilvl=ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_smb3_fs_context)

# vim: sw=4 ts=4 noexpandtab
