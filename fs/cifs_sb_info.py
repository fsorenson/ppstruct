#!/usr/bin/python

from __future__ import print_function
from fs_lib import *

CIFS_MOUNT_FLAGS_C = '''
#define CIFS_MOUNT_NO_PERM          0
#define CIFS_MOUNT_SET_UID          1
#define CIFS_MOUNT_SERVER_INUM      2
#define CIFS_MOUNT_DIRECT_IO        3
#define CIFS_MOUNT_NO_XATTR         4
#define CIFS_MOUNT_MAP_SPECIAL_CHR  5
#define CIFS_MOUNT_POSIX_PATHS      6
#define CIFS_MOUNT_UNX_EMUL         7
#define CIFS_MOUNT_NO_BRL           8
#define CIFS_MOUNT_CIFS_ACL         9
#define CIFS_MOUNT_OVERR_UID        10
#define CIFS_MOUNT_OVERR_GID        11
#define CIFS_MOUNT_DYNPERM          12
#define CIFS_MOUNT_NOPOSIXBRL       13
#define CIFS_MOUNT_NOSSYNC          14
#define CIFS_MOUNT_FSCACHE          15
#define CIFS_MOUNT_MF_SYMLINKS      16
#define CIFS_MOUNT_MULTIUSER        17
#define CIFS_MOUNT_STRICT_IO        18
#define CIFS_MOUNT_RWPIDFORWARD     19
#define CIFS_MOUNT_POSIXACL         20
#define CIFS_MOUNT_MAP_SFM_CHR      23
'''
CIFS_MOUNT_FLAGS = CDefine(CIFS_MOUNT_FLAGS_C)

@struct_label_string(("prepath", "ctx.source", "ctx.UNC"))
@struct_printer
def pp_struct_cifs_sb_info(csbi, rlvl, ilvl):

	if csbi.hasField("prepath") and csbi.prepath:
		try:
			print("{}.prepath = '{}'".format(indent_str(ilvl), csbi.prepath))
		except:
			pass

	if csbi.hasField("mnt_cifs_flags"):
		try:
			flags_val = int(csbi.mnt_cifs_flags.counter)
			str_flags = flags_to_string(flags_val, CIFS_MOUNT_FLAGS)
			print("{}.mnt_cifs_flags = 0x{:x} - {}".format(indent_str(ilvl), flags_val, str_flags))
		except:
			pass

	if csbi.hasField("active"):
		try:
			act = int(csbi.active.counter)
			print("{}.active = {}".format(indent_str(ilvl), act))
		except:
			pass

	if csbi.hasField("outstanding_rreq"):
		try:
			reqs = int(csbi.outstanding_rreq.counter)
			if reqs != 0:
				print("{}.outstanding_rreq = {}".format(indent_str(ilvl), reqs))
		except:
			pass

	if csbi.hasField("mnt_cifs_serverino_autodisabled") and csbi.mnt_cifs_serverino_autodisabled:
		print("{}.mnt_cifs_serverino_autodisabled = True".format(indent_str(ilvl)))

	# Context (struct smb3_fs_context)
	if csbi.hasField("ctx") and csbi.ctx and long(csbi.ctx) != 0:
		pp_struct_member(csbi, "ctx", rlvl=rlvl, ilvl=ilvl)

	# Master Tree Connect Link (struct tcon_link)
	if csbi.hasField("master_tlink") and csbi.master_tlink and long(csbi.master_tlink) != 0:
		pp_struct_member(csbi, "master_tlink", rlvl=rlvl, ilvl=ilvl)

	# Local NLS table
	if csbi.hasField("local_nls") and csbi.local_nls and long(csbi.local_nls) != 0:
		pp_struct_member(csbi, "local_nls", rlvl=rlvl, ilvl=ilvl)

	# Root dentry
	if csbi.hasField("root") and csbi.root and long(csbi.root) != 0:
		pp_struct_member(csbi, "root", rlvl=0, ilvl=ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_cifs_sb_info)

# vim: sw=4 ts=4 noexpandtab
