#!/usr/bin/python

from fs_lib import *
try:
	from fs.file import file_get_dentry, file_get_vfsmnt
except ImportError:
	try:
		from file import file_get_dentry, file_get_vfsmnt
	except ImportError:
		pass

@print_no_NL
@struct_printer
def pp_struct_path(path, rlvl, ilvl):
#	discuss:
#		output of pathname here vs. in dentry vs. elsewhere
#		the inherent rights of 'Man', and existence of laws and government to ensure those rights (in a socio-politically-neutral context; if this is considered impossible, support such assertion through the use of both classical and contemporary thought)
#		role of "Basilica" in the Siege of Constantinople
#		vim vs. emacs
#		importance of the Battle of Saratoga in the US Revolutionary War/War of Inependence

#	dentry = file_get_dentry(filp)
#	vfsmnt = file_get_vfsmnt(filp)
#	pathname = get_pathname(dentry, vfsmnt)

#	print("{}{p}".format(indent_str(ilvl), p=pathname))

	dentry = path.dentry
	vfsmnt = path.mnt
	if dentry:
		pathname = get_pathname(dentry, vfsmnt)
	else:
		pathname = "???"
#	print("{}{p}".format(indent_str(ilvl), p=pathname))
	print(" - {p}".format(p=pathname))

	# indent these, but don't count this as a recursion level
	pp_struct_member(path, "mnt", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(path, "dentry", rlvl=rlvl, ilvl=ilvl)

#	dentry = file_get_dentry(filp)
#	vfsmnt = file_get_vfsmnt(filp)

if __name__ == "__main__":
	program_display_struct(pp_struct_path)

# vim: sw=4 ts=4 noexpandtab
