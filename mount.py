#!/usr/bin/python

from fs_lib import *
from fs.common import *

@struct_label_string_quiet_fail
@struct_label_string('mnt_devname')
@struct_printer
def pp_struct_mount(mount, rlvl, ilvl):
	parts = []
	if mount.hasField("mnt_id"):
		parts.append(".mnt_id = {}".format(mount.mnt_id))
	if mount.hasField("mnt_group_id") and mount.mnt_group_id != 0:
		parts.append(".mnt_group_id = {}".format(mount.mnt_group_id))
	if parts:
		print(indent_str(ilvl) + ", ".join(parts))

	if mount.hasField("mnt"):
		mnt_flags = mount.mnt.mnt_flags
		print("{}.mnt_flags = 0x{fl:x} - {str}".format(indent_str(ilvl), fl=mnt_flags, str=show_mnt_flags_strings(mnt_flags)))
	elif mount.hasField("mnt_flags"):
		mnt_flags = mount.mnt_flags
		print("{}.mnt_flags = 0x{fl:x} - {str}".format(indent_str(ilvl), fl=mnt_flags, str=show_mnt_flags_strings(mnt_flags)))

	if mount.hasField("mnt_parent"):
		if long(mount.mnt_parent) == long(mount):
			print("{}.mnt_parent(struct mount *)0x{:x} - (self/root)".format(indent_str(ilvl), long(mount.mnt_parent)))
		else:
			pp_struct_member(mount, "mnt_parent", rlvl=rlvl, ilvl=ilvl)

	if mount.hasField("mnt_mountpoint"):
		pp_struct_member(mount, "mnt_mountpoint", rlvl=rlvl, ilvl=ilvl)

	if mount.hasField("mnt"):
		pp_struct_member(mount.mnt, "mnt_root", rlvl=rlvl, ilvl=ilvl)
		pp_struct_member(mount.mnt, "mnt_sb", rlvl=rlvl, ilvl=ilvl)
	else:
		if mount.hasField("mnt_root"):
			pp_struct_member(mount, "mnt_root", rlvl=rlvl, ilvl=ilvl)
		if mount.hasField("mnt_sb"):
			pp_struct_member(mount, "mnt_sb", rlvl=rlvl, ilvl=ilvl)

	if mount.hasField("mnt_master") and long(mount.mnt_master) != 0:
		pp_struct_member(mount, "mnt_master", rlvl=rlvl, ilvl=ilvl)

	if mount.hasField("mnt_ns") and long(mount.mnt_ns) != 0:
		pp_struct_member(mount, "mnt_ns", rlvl=rlvl, ilvl=ilvl)

	if ppstruct_vars.pp_struct_opts.counts:
		if mount.hasField("mnt_count"):
			print("{ind}{c}".format(indent_str(ilvl), c=pp_member_val(mount, "mnt_count")))
		elif mount.hasField("mnt") and mount.mnt.hasField("mnt_count"):
			print("{ind}{c}".format(indent_str(ilvl), c=pp_member_val(mount.mnt, "mnt_count")))

if __name__ == "__main__":
	program_display_struct(pp_struct_mount)
