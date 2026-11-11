#!/usr/bin/python

from fs_lib import *
from fs.common import *

@struct_label_string_quiet_fail
@struct_label_string('mnt_devname')
@struct_printer
def pp_struct_vfsmount(vfsmount, rlvl, ilvl):
	try:
		mnt = container_of(vfsmount, "struct mount", "mnt")
	except:
		mnt = vfsmount

	mnt_flags = vfsmount.mnt_flags
	print("{}.mnt_flags = 0x{fl:x} - {str}".format(indent_str(ilvl), fl=mnt_flags, str=show_mnt_flags_strings(mnt_flags)))
	# indent these, but don't count this as a recursion level
	if struct__has_member("mount", "mnt_parent"):
		pp_struct_member(mnt, "mnt_parent", rlvl=rlvl, ilvl=ilvl)
	else:
		pp_struct_member(vfsmount, "mnt_parent", rlvl=rlvl, ilvl=ilvl)

	pp_struct_member(vfsmount, "mnt_root", rlvl=rlvl, ilvl=ilvl)

	if struct__has_member("mount", "mnt_mountpoint"):
		pp_struct_member(mnt, "mnt_mountpoint", rlvl=rlvl, ilvl=ilvl)
	else:
		pp_struct_member(vfsmount, "mnt_mountpoint", rlvl=rlvl, ilvl=ilvl)

	pp_struct_member(vfsmount, "mnt_sb", rlvl=rlvl, ilvl=ilvl)

	if struct__has_member("mount", "mnt_ns"):
		pp_struct_member(mnt, "mnt_ns", rlvl=rlvl, ilvl=ilvl)
	else:
		pp_struct_member(vfsmount, "mnt_ns", rlvl=rlvl, ilvl=ilvl)

	if ppstruct_vars.pp_struct_opts.counts:
		c_src = mnt if struct__has_member("mount", "mnt_count") else vfsmount
		print("{ind}{c}".format(indent_str(ilvl), c=pp_member_val(c_src, "mnt_count")))



if __name__ == "__main__":
	program_display_struct(pp_struct_vfsmount)

# vim: sw=4 ts=4 noexpandtab
