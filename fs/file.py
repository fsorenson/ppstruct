#!/usr/bin/python

from __future__ import print_function

from fs_lib import *



if struct__has_member("file", "f_path"):
	def file_get_dentry(filp):
		try:
			return Deref(filp.f_path.dentry)
		except:
			return 0
	def file_get_vfsmnt(filp):
		try:
			return Deref(filp.f_path.mnt)
		except:
			return 0
else:
	def file_get_dentry(filp):
		try:
			return Deref(filp.f_dentry)
		except:
			return 0
	def file_get_vfsmnt(filp):
		try:
			return Deref(filp.f_vfsmnt)
		except:
			return 0


F_MODE_C = '''
#define READ		0
#define WRITE		1
#define LSEEK		2
#define PREAD		3
#define PWRITE		4
#define EXEC		5
#define NDELAY		6
#define EXCL		7
#define WRITE_IOCTL	8
'''
F_MODE = CDefine(F_MODE_C)

F_FLAGS_C = '''
#define O_CREAT		6
#define O_EXCL		7
#define O_NOCTTY	8
#define O_TRUNC		9
#define O_APPEND	10
#define O_NONBLOCK	11
#define O_DSYNC		12
#define O_FASYNC	13
#define O_DIRECT	14
#define O_LARGEFILE	15
#define O_DIRECTORY	16
#define O_NOFOLLOW	17
#define O_NOATIME	18
#define O_CLOEXEC	19
#define O_SYNC		20
#define O_PATH		21
#define O_TMPFILE	22
'''
F_FLAGS = CDefine(F_FLAGS_C)

O_ACCMODE = 0o00000003
def OPEN_FMODE(flag):
	return ((flag + 1) & O_ACCMODE)
FMODE_READ = (1)
FMODE_WRITE = (2)

def open_mode_string(open_mode):
	if (open_mode & (F_MODE.READ | F_MODE.WRITE)) == (F_MODE.READ | F_MODE.WRITE):
		return "O_RDWR"
	if (open_mode & F_MODE.READ) == F_MODE.READ:
		return "O_RDONLY"
	return "O_WRONLY"

@struct_printer
def pp_struct_file(filp, rlvl, ilvl):
	dentry = file_get_dentry(filp)
	vfsmnt = file_get_vfsmnt(filp)
#	print("dentry: {:016x}, vfsmnt: {:016x}".format(dentry, vfsmnt))

	if dentry:
		pathname = get_pathname(dentry, vfsmnt)
	else:
		pathname = "???"

	pp_struct_member(filp, "f_path", rlvl=rlvl, ilvl=ilvl)
	print("{}{p}".format(indent_str(ilvl), p=pathname))
	pp_struct_member(filp, "f_inode", rlvl=rlvl, ilvl=ilvl)

#	print("{}dentry = 0x{d:016x}, vfsmount = 0x{v:016x}".format(indent_str(ilvl), d=dentry, v=vfsmnt))
	if dentry:
		print("{}.f_{}dentry - ".format(indent_str(ilvl), '{path.}'), end='')
		pp_struct("dentry", dentry, rlvl=rlvl, ilvl=ilvl)

	f_mode = filp.f_mode
	f_flags = filp.f_flags
	open_mode = OPEN_FMODE(f_mode)
#	open_mode = OPEN_FMODE(f_flags)
#	open_mode = f_mode
	f_mode = f_mode & ~O_ACCMODE

	print("{}OPEN_MODE: {om}, .f_pos: {pos}".format(indent_str(ilvl), om=open_mode_string(open_mode), pos=filp.f_pos))

#	print("\t.f_mode = 0x%x - %s" % (f_mode, file_mode_string(f_mode))
	print("{}.f_mode = 0x{m:x} - {f}".format(indent_str(ilvl), m=f_mode, f=flags_to_string(f_mode, F_MODE)))

	print("{}.f_flags = 0x{f:x} - {s}".format(indent_str(ilvl), f=f_flags, s=flags_to_string(f_flags, F_FLAGS)))

	pp_struct_member(filp, "f_mapping", rlvl=rlvl, ilvl=ilvl)


if __name__ == "__main__":
	program_display_struct(pp_struct_file)

# vim: sw=4 ts=4 noexpandtab
