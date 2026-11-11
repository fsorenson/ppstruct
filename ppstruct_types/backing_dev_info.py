#!/usr/bin/python

from __future__ import print_function

from fs_lib import *
from LinuxDump.percpu import percpu_counter_sum

# Modern capabilities (kernel 4.2+)
# flags_to_string expects bit numbers (0, 1, 2...)
BDI_CAPS_MODERN_C = '''
#define BDI_CAP_WRITEBACK       0
#define BDI_CAP_STRICTLIMIT     1
'''
BDI_CAPS_MODERN = CDefine(BDI_CAPS_MODERN_C)

# Legacy capabilities (older kernels)
BDI_CAPS_LEGACY_C = '''
#define BDI_CAP_NO_ACCT_DIRTY   0
#define BDI_CAP_NO_WRITEBACK    1
#define BDI_CAP_MAP_COPY        2
#define BDI_CAP_MAP_DIRECT      3
#define BDI_CAP_READ_MAP        4
#define BDI_CAP_WRITE_MAP       5
#define BDI_CAP_EXEC_MAP        6
#define BDI_CAP_NO_ACCT_WB      7
#define BDI_CAP_SWAP_BACKED     8
#define BDI_CAP_STABLE_WRITES   9
#define BDI_CAP_STRICTLIMIT     10
'''
BDI_CAPS_LEGACY = CDefine(BDI_CAPS_LEGACY_C)

@struct_label_string(("dev_name", "name"))
@struct_printer
def pp_struct_backing_dev_info(bdi, rlvl, ilvl):

	if bdi.hasField("capabilities"):
		caps = int(bdi.capabilities)
		if bdi.hasField("wb"):
			s = flags_to_string(caps, BDI_CAPS_MODERN)
		else:
			s = flags_to_string(caps, BDI_CAPS_LEGACY)
		print("{}.capabilities = 0x{c:x} - {s}".format(indent_str(ilvl), c=caps, s=s))

	# Legacy state if wb is not present
	if not bdi.hasField("wb") and bdi.hasField("state"):
		try:
			print("{}.state = ".format(indent_str(ilvl)), end='')
			print_enum_bit(bdi.state, "bdi_state")
		except:
			print("{}.state = 0x{:x}".format(indent_str(ilvl), int(bdi.state)))

	if bdi.hasField("ra_pages"):
		ra_pages = int(bdi.ra_pages)
		ra_bytes = ra_pages * 4096
		print("{}.ra_pages = {} ({})".format(
			indent_str(ilvl), ra_pages, val_to_units_string(ra_bytes, 1024)))

	if bdi.hasField("io_pages"):
		io_pages = int(bdi.io_pages)
		io_bytes = io_pages * 4096
		print("{}.io_pages = {} ({})".format(
			indent_str(ilvl), io_pages, val_to_units_string(io_bytes, 1024)))

	if bdi.hasField("min_ratio"):
		pp_struct_member(bdi, "min_ratio", ilvl=ilvl)
	if bdi.hasField("max_ratio"):
		pp_struct_member(bdi, "max_ratio", ilvl=ilvl)

	# Writeback structure or legacy writeback fields
	if bdi.hasField("wb"):
		pp_struct_member(bdi, "wb", rlvl=rlvl, ilvl=ilvl)
	else:
		if bdi.hasField("write_bandwidth"):
			pp_struct_member(bdi, "write_bandwidth", ilvl=ilvl)
		if bdi.hasField("avg_write_bandwidth"):
			pp_struct_member(bdi, "avg_write_bandwidth", ilvl=ilvl)
		if bdi.hasField("dirty_exceeded"):
			pp_struct_member(bdi, "dirty_exceeded", ilvl=ilvl)
		if bdi.hasField("dirty_ratelimit"):
			pp_struct_member(bdi, "dirty_ratelimit", ilvl=ilvl)

	# Devices
	if bdi.hasField("dev") and bdi.dev and long(bdi.dev) != 0:
		pp_struct_member(bdi, "dev", rlvl=rlvl, ilvl=ilvl)

	if bdi.hasField("owner") and bdi.owner and long(bdi.owner) != 0:
		pp_struct_member(bdi, "owner", rlvl=rlvl, ilvl=ilvl)

	# Debugfs directory (non-recursive to avoid deep dentry recursion)
	if bdi.hasField("debug_dir") and bdi.debug_dir and long(bdi.debug_dir) != 0:
		pp_struct_member(bdi, "debug_dir", rlvl=0, ilvl=ilvl)

	# Legacy bdi_stat
	if bdi.hasField("bdi_stat"):
		try:
			bdi_stat_item = EnumInfo("enum bdi_stat_item")
			print("{}.bdi_stat:".format(indent_str(ilvl)))
			for i in range(0, bdi_stat_item.NR_BDI_STAT_ITEMS):
				try:
					print("{}[{}]: {}".format(indent_str(ilvl+1), bdi_stat_item.getnam(i), percpu_counter_sum(bdi.bdi_stat[i])))
				except Exception as e:
					print("exception getting bdi_stat[{}]: {}".format(i, e))
		except:
			pass

if __name__ == "__main__":
	program_display_struct(pp_struct_backing_dev_info)

# vim: sw=4 ts=4 noexpandtab
