#!/usr/bin/python

from __future__ import print_function
from fs_lib import *

NFS_MOUNT_FLAGS_C = '''
#define NFS_MOUNT_SOFT              0
#define NFS_MOUNT_INTR              1
#define NFS_MOUNT_SECURE            2
#define NFS_MOUNT_POSIX             3
#define NFS_MOUNT_NOCTO             4
#define NFS_MOUNT_NOAC              5
#define NFS_MOUNT_TCP               6
#define NFS_MOUNT_VER3              7
#define NFS_MOUNT_KERBEROS          8
#define NFS_MOUNT_NONLM             9
#define NFS_MOUNT_BROKEN_SUID       10
#define NFS_MOUNT_NOACL             11
#define NFS_MOUNT_STRICTLOCK        12
#define NFS_MOUNT_SECFLAVOUR        13
#define NFS_MOUNT_NORDIRPLUS        14
#define NFS_MOUNT_UNSHARED          15
#define NFS_MOUNT_LOOKUP_CACHE_NONEG 16
#define NFS_MOUNT_LOOKUP_CACHE_NONE  17
#define NFS_MOUNT_NORESVPORT        18
#define NFS_MOUNT_LEGACY_INTERFACE  19
#define NFS_MOUNT_LOCAL_FLOCK       20
#define NFS_MOUNT_LOCAL_FCNTL       21
#define NFS_MOUNT_SOFTERR           22
#define NFS_MOUNT_SOFTREVAL         23
#define NFS_MOUNT_WRITE_EAGER       24
#define NFS_MOUNT_WRITE_WAIT        25
#define NFS_MOUNT_TRUNK_DISCOVERY   26
#define NFS_MOUNT_SHUTDOWN          27
#define NFS_MOUNT_NO_ALIGNWRITE     28
#define NFS_MOUNT_FORCE_RDIRPLUS    29
#define NFS_MOUNT_NETUNREACH_FATAL  30
'''
NFS_MOUNT_FLAGS = CDefine(NFS_MOUNT_FLAGS_C)

NFS_CAP_FLAGS_C = '''
#define NFS_CAP_READDIRPLUS         0
#define NFS_CAP_HARDLINKS           1
#define NFS_CAP_SYMLINKS            2
#define NFS_CAP_ACLS                3
#define NFS_CAP_ATOMIC_OPEN         4
#define NFS_CAP_LGOPEN              5
#define NFS_CAP_CASE_INSENSITIVE    6
#define NFS_CAP_CASE_PRESERVING     7
#define NFS_CAP_REBOOT_LAYOUTRETURN 8
#define NFS_CAP_OFFLOAD_STATUS      9
#define NFS_CAP_ZERO_RANGE          10
#define NFS_CAP_DIR_DELEG           11
#define NFS_CAP_OPEN_XOR            12
#define NFS_CAP_DELEGTIME           13
#define NFS_CAP_POSIX_LOCK          14
#define NFS_CAP_UIDGID_NOMAP        15
#define NFS_CAP_STATEID_NFSV41      16
#define NFS_CAP_ATOMIC_OPEN_V1      17
#define NFS_CAP_SECURITY_LABEL      18
#define NFS_CAP_SEEK                19
#define NFS_CAP_ALLOCATE            20
#define NFS_CAP_DEALLOCATE          21
#define NFS_CAP_LAYOUTSTATS         22
#define NFS_CAP_CLONE               23
#define NFS_CAP_COPY                24
#define NFS_CAP_OFFLOAD_CANCEL      25
#define NFS_CAP_LAYOUTERROR         26
#define NFS_CAP_COPY_NOTIFY         27
#define NFS_CAP_XATTR               28
#define NFS_CAP_READ_PLUS           29
#define NFS_CAP_FS_LOCATIONS        30
#define NFS_CAP_MOVEABLE            31
'''
NFS_CAP_FLAGS = CDefine(NFS_CAP_FLAGS_C)

@struct_label_string(("nfs_client.cl_hostname", "fscache_uniq"))
@struct_printer
def pp_struct_nfs_server(nfs_s, rlvl, ilvl):

	if nfs_s.hasField("s_dev") and nfs_s.s_dev:
		dev = int(nfs_s.s_dev)
		maj = dev >> 20
		min = dev & 0xfffff
		print("{}.s_dev = {}:{} (0x{:x})".format(indent_str(ilvl), maj, min, dev))

	if nfs_s.hasField("fsid"):
		try:
			major = int(nfs_s.fsid.major)
			minor = int(nfs_s.fsid.minor)
			print("{}.fsid = 0x{:x}:0x{:x}".format(indent_str(ilvl), major, minor))
		except:
			pass

	if nfs_s.hasField("flags") and nfs_s.flags:
		try:
			fl = int(nfs_s.flags)
			fl_str = flags_to_string(fl, NFS_MOUNT_FLAGS)
			print("{}.flags = 0x{:x} - {}".format(indent_str(ilvl), fl, fl_str))
		except:
			pass

	if nfs_s.hasField("caps") and nfs_s.caps:
		try:
			cp = int(nfs_s.caps)
			cp_str = flags_to_string(cp, NFS_CAP_FLAGS)
			print("{}.caps = 0x{:x} - {}".format(indent_str(ilvl), cp, cp_str))
		except:
			pass

	# Buffer & I/O sizes
	io_sizes = []
	for f in ["rsize", "wsize", "dtsize", "bsize"]:
		if nfs_s.hasField(f) and getattr(nfs_s, f):
			val = int(getattr(nfs_s, f))
			io_sizes.append("{}: {} ({})".format(f, val, val_to_units_string(val, 1024)))
	if io_sizes:
		print("{}.io_sizes: {}".format(indent_str(ilvl), ", ".join(io_sizes)))

	if nfs_s.hasField("rpages") and nfs_s.rpages:
		print("{}.rpages = {}".format(indent_str(ilvl), int(nfs_s.rpages)))

	if nfs_s.hasField("port") and nfs_s.port:
		print("{}.port = {}".format(indent_str(ilvl), int(nfs_s.port)))

	if nfs_s.hasField("acregmin") and nfs_s.hasField("acregmax"):
		try:
			reg_min = int(nfs_s.acregmin)
			reg_max = int(nfs_s.acregmax)
			dir_min = int(nfs_s.acdirmin)
			dir_max = int(nfs_s.acdirmax)
			print("{}.ac_timeout: file={}s..{}s, dir={}s..{}s (acreg={}/{}, acdir={}/{})".format(
				indent_str(ilvl), reg_min // 1000, reg_max // 1000, dir_min // 1000, dir_max // 1000,
				reg_min, reg_max, dir_min, dir_max
			))
		except:
			pass

	if nfs_s.hasField("namelen") and nfs_s.namelen:
		print("{}.namelen = {}".format(indent_str(ilvl), int(nfs_s.namelen)))

	if nfs_s.hasField("fscache_uniq") and nfs_s.fscache_uniq and not is_err_or_null(nfs_s.fscache_uniq):
		try:
			print("{}.fscache_uniq = '{}'".format(indent_str(ilvl), nfs_s.fscache_uniq))
		except:
			pass

	if nfs_s.hasField("active"):
		try:
			act = int(nfs_s.active.counter)
			print("{}.active = {}".format(indent_str(ilvl), act))
		except:
			pass

	# Sub-structures
	if nfs_s.hasField("nfs_client") and not is_err_or_null(nfs_s.nfs_client):
		pp_struct_member(nfs_s, "nfs_client", rlvl=rlvl, ilvl=ilvl)

	if nfs_s.hasField("client") and not is_err_or_null(nfs_s.client):
		pp_struct_member(nfs_s, "client", rlvl=rlvl, ilvl=ilvl)

	if nfs_s.hasField("client_acl"):
		if is_err_or_null(nfs_s.client_acl):
			val = int(nfs_s.client_acl)
			if val != 0:
				err = get_err_code(val)
				print("{}.client_acl (struct rpc_clnt *)0x{:016x} - ERR_PTR({})".format(
					indent_str(ilvl), val & 0xffffffffffffffff, err))
		else:
			pp_struct_member(nfs_s, "client_acl", rlvl=rlvl, ilvl=ilvl)

	if nfs_s.hasField("nlm_host") and not is_err_or_null(nfs_s.nlm_host):
		pp_struct_member(nfs_s, "nlm_host", rlvl=rlvl, ilvl=ilvl)

	if nfs_s.hasField("pnfs_curr_ld") and not is_err_or_null(nfs_s.pnfs_curr_ld):
		pp_struct_member(nfs_s, "pnfs_curr_ld", rlvl=rlvl, ilvl=ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_nfs_server)

# vim: sw=4 ts=4 noexpandtab
