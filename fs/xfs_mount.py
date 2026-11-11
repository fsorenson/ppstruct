#!/usr/bin/python
from fs_lib import *

XFS_SB_VERSION_5 = 5

__XFS_SB_VERSION_FLAGS = '''
#define XFS_SB_VERSION_NUMBITS         0x000f
#define XFS_SB_VERSION_ALLFBITS        0xfff0
#define XFS_SB_VERSION_ATTRBIT         0x0010
#define XFS_SB_VERSION_NLINKBIT        0x0020
#define XFS_SB_VERSION_QUOTABIT        0x0040
#define XFS_SB_VERSION_ALIGNBIT        0x0080
#define XFS_SB_VERSION_DALIGNBIT       0x0100
#define XFS_SB_VERSION_SHAREDBIT       0x0200
#define XFS_SB_VERSION_LOGV2BIT        0x0400
#define XFS_SB_VERSION_SECTORBIT       0x0800
#define XFS_SB_VERSION_EXTFLGBIT       0x1000
#define XFS_SB_VERSION_DIRV2BIT        0x2000
#define XFS_SB_VERSION_BORGBIT         0x4000
#define XFS_SB_VERSION_MOREBITSBIT     0x8000
'''
XFS_SB_VERSION_FLAGS = CDefine(__XFS_SB_VERSION_FLAGS)

__XFS_SB_VERSION2_FLAGS = '''
#define XFS_SB_VERSION2_LAZYSBCOUNTBIT  0x00000002
#define XFS_SB_VERSION2_ATTR2BIT        0x00000008
#define XFS_SB_VERSION2_PROJID32BIT     0x00000080
#define XFS_SB_VERSION2_CRCBIT          0x00000100
#define XFS_SB_VERSION2_FTYPE           0x00000200
'''
XFS_SB_VERSION2_FLAGS = CDefine(__XFS_SB_VERSION2_FLAGS)

__XFS_SB_FEAT_FLAGS = '''
#define XFS_SB_FEAT_RO_COMPAT_FINOBT   0x1
#define XFS_SB_FEAT_RO_COMPAT_RMAPBT   0x2
#define XFS_SB_FEAT_RO_COMPAT_REFLINK  0x4
#define XFS_SB_FEAT_INCOMPAT_FTYPE      0x1
#define XFS_SB_FEAT_INCOMPAT_SPINODES   0x2
#define XFS_SB_FEAT_INCOMPAT_META_UUID  0x4
'''
XFS_SB_FEAT_FLAGS = CDefine(__XFS_SB_FEAT_FLAGS)

def XFS_SB_VERSION_NUM(sbp):
	return sbp.sb_versionnum & XFS_SB_VERSION_FLAGS['XFS_SB_VERSION_NUMBITS']

def xfs_sb_version(sbp, flagname):
	flagname = "XFS_SB_VERSION_" + flagname
	return 1 if (sbp.sb_versionnum & XFS_SB_VERSION_FLAGS[flagname]) else 0

def xfs_sb_version2(sbp, flagname):
	flagname = "XFS_SB_VERSION2_" + flagname
	return 1 if (sbp.sb_features2 & XFS_SB_VERSION2_FLAGS[flagname]) else 0

def xfs_sb_has_ro_compat_feat(sbp, flagname):
	flagname = "XFS_SB_FEAT_RO_COMPAT_" + flagname
	return 1 if (sbp.sb_features_ro_compat & XFS_SB_FEAT_FLAGS[flagname]) else 0

def xfs_sb_has_incompat_feat(sbp, flagname):
	try:
		flagname = "XFS_SB_FEAT_INCOMPAT_" + flagname
		return 1 if (sbp.sb_features_incompat & XFS_SB_FEAT_FLAGS[flagname]) else 0
	except:
		return 0

def xfs_sb_version_hasmorebits(sbp):
	if XFS_SB_VERSION_NUM(sbp) == XFS_SB_VERSION_5:
		return 1
	return 1 if (sbp.sb_versionnum & XFS_SB_VERSION_FLAGS['XFS_SB_VERSION_MOREBITSBIT']) else 0

def xfs_sb_version_hascrc(sbp):
	return 1 if (XFS_SB_VERSION_NUM(sbp) == XFS_SB_VERSION_5) else 0

def xfs_sb_version_hasfinobt(sbp):
	return 1 if (XFS_SB_VERSION_NUM(sbp) == XFS_SB_VERSION_5 and xfs_sb_has_ro_compat_feat(sbp, 'FINOBT')) else 0

def xfs_sb_version_hasprojid32bit(sbp):
	if XFS_SB_VERSION_NUM(sbp) == XFS_SB_VERSION_5:
		return 1
	return 1 if (xfs_sb_version_hasmorebits(sbp) and xfs_sb_version2(sbp, 'PROJID32BIT')) else 0

def xfs_sb_version_hasftype(sbp):
	if XFS_SB_VERSION_NUM(sbp) == XFS_SB_VERSION_5 and xfs_sb_has_incompat_feat(sbp, "FTYPE"):
		return 1
	if xfs_sb_version(sbp, "MOREBITSBIT") and xfs_sb_version2(sbp, "FTYPE"):
		return 1
	return 0

def xfs_version_haslogv2(sbp):
	if XFS_SB_VERSION_NUM(sbp) == XFS_SB_VERSION_5:
		return 1
	return 1 if xfs_sb_version(sbp, "LOGV2BIT") else 0

def xfs_sb_version_hasreflink(sbp):
	return 1 if (XFS_SB_VERSION_NUM(sbp) == XFS_SB_VERSION_5 and xfs_sb_has_ro_compat_feat(sbp, "REFLINK")) else 0

def super_block_devname(sb):
	try:
		sb = readSU("struct super_block", sb)
		first_mount = readSU("struct mount", container_of(sb.s_mounts.next, "struct mount", "mnt_instance"))
		return first_mount.mnt_devname
	except:
		try:
			return sb.s_id
		except:
			return "UNKNOWN"

def print_xfs_info(mp, ilvl=0):
	sbp = mp.m_sb
	ind = indent_str(ilvl)
	print("{}super block version {}".format(ind, XFS_SB_VERSION_NUM(sbp)))
	if sbp.hasField("sb_inprogress") and sbp.sb_inprogress:
		print("{}***** WARNING: superblock sb_inprogress flag is set: {} *****".format(ind, sbp.sb_inprogress))

	devname = super_block_devname(mp.m_super) if mp.hasField("m_super") and mp.m_super else "UNKNOWN"
	print("{}meta-data={:<22s} isize={:<6d} agcount={}, agsize={} blks".format(
		ind, devname, sbp.sb_inodesize, sbp.sb_agcount, sbp.sb_agblocks))

	attr_version = 2 if xfs_sb_version2(sbp, "ATTR2BIT") else 1 if xfs_sb_version(sbp, "ATTRBIT") else 0
	print("{}         ={:<22s} sectsz={:<5d} attr={}, projid32bit={}".format(ind, "",
		sbp.sb_sectsize, attr_version, xfs_sb_version_hasprojid32bit(sbp)))

	print("{}         ={:<22s} crc={:<8d} finobt={} spinodes={}".format(ind, "",
		xfs_sb_version_hascrc(sbp), xfs_sb_version_hasfinobt(sbp), xfs_sb_has_incompat_feat(sbp, "SPINODES")))

	print("{}         ={:<22s} reflink={}".format(ind, "", xfs_sb_version_hasreflink(sbp)))

	print("{}         ={:<22s} bsize={:<6d} blocks={}, imaxpct={}".format(ind, "",
		sbp.sb_blocksize, sbp.sb_dblocks, sbp.sb_imax_pct))

	swidth = mp.m_swidth if mp.hasField("m_swidth") else 0
	print("{}         ={:<22s} sunit={:<6d} swidth={} blks".format(ind, "",
		sbp.sb_unit, swidth))

	dirversion = 2 if xfs_sb_version(sbp, "DIRV2BIT") else 1
	dirblksize = 0
	if mp.hasField("m_dir_geo") and mp.m_dir_geo and mp.m_dir_geo.hasField("blksize"):
		dirblksize = mp.m_dir_geo.blksize
	elif mp.hasField("m_dirblksize"):
		dirblksize = mp.m_dirblksize
	else:
		dirblksize = 1 << (sbp.sb_blocklog + sbp.sb_dirblklog) if sbp.hasField("sb_dirblklog") else sbp.sb_blocksize

	print("{}naming   =version {:<14d} bsize={:<6d} ascii-ci={} ftype={}".format(
		ind, dirversion, dirblksize, xfs_sb_version(sbp, "BORGBIT"), xfs_sb_version_hasftype(sbp)))

	logname = mp.m_logname if mp.hasField("m_logname") else None
	int_ext = "internal" if logname is None or logname == "" else "external"
	logversion = 2 if xfs_version_haslogv2(sbp) else 1
	print("{}log      ={:<22s} bsize={:<6d} blocks={}, version={}".format(
		ind, int_ext, 1 << sbp.sb_blocklog, sbp.sb_logblocks, logversion))

	print("{}         ={:<22s} sectsz={:<5d} sunit={} blks, lazy-count={}".format(ind, "",
		sbp.sb_logsectsize, sbp.sb_logsunit, xfs_sb_version2(sbp, "LAZYSBCOUNTBIT")))

	rtname = "none" if sbp.sb_rblocks == 0 else "external" if not mp.hasField("m_rtname") or mp.m_rtname is None else mp.m_rtname
	print("{}realtime ={:<22s} extsz={:<6d} blocks={}, rtextents={}".format(ind, rtname,
		sbp.sb_rextsize, sbp.sb_rblocks, sbp.sb_rextents))

@struct_label_string_quiet_fail
@struct_label_string('m_super.s_id')
@struct_printer
def pp_struct_xfs_mount(mp, rlvl, ilvl):
	sb = mp.m_sb
	bsize = sb.sb_blocksize
	dblocks = sb.sb_dblocks
	fname = sb.sb_fname if hasattr(sb, 'sb_fname') else ''
	if fname:
		print("{}.sb_fname = '{}'".format(indent_str(ilvl), fname))

	# Filesystem geometry & sizing
	print("{}.sb_blocksize = {}, .sb_dblocks = {} ({})".format(
		indent_str(ilvl), bsize, dblocks, val_to_units_string(dblocks * bsize, 1024)))
	print("{}.sb_agcount = {}, .sb_agblocks = {}".format(
		indent_str(ilvl), sb.sb_agcount, sb.sb_agblocks))
	print("{}.sb_inodesize = {}, .sb_inopblock = {}".format(
		indent_str(ilvl), sb.sb_inodesize, sb.sb_inopblock))

	# Allocation & free space stats
	print("{}.sb_icount = {}, .sb_ifree = {}".format(
		indent_str(ilvl), sb.sb_icount, sb.sb_ifree))
	print("{}.sb_fdblocks = {} ({} free)".format(
		indent_str(ilvl), sb.sb_fdblocks, val_to_units_string(sb.sb_fdblocks * bsize, 1024)))

	# xfs_info-style summary
	print_xfs_info(mp, ilvl=ilvl)

	# Connected structures
	pp_struct_member(mp, "m_ddev_targp", rlvl=rlvl, ilvl=ilvl)
	if mp.hasField("m_logdev_targp") and mp.m_logdev_targp and mp.m_logdev_targp != mp.m_ddev_targp:
		pp_struct_member(mp, "m_logdev_targp", rlvl=rlvl, ilvl=ilvl)
	if mp.hasField("m_rtdev_targp") and mp.m_rtdev_targp:
		pp_struct_member(mp, "m_rtdev_targp", rlvl=rlvl, ilvl=ilvl)

	pp_struct_member(mp, "m_rootip", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(mp, "m_super", rlvl=rlvl, ilvl=ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_xfs_mount)

# vim: sw=4 ts=4 noexpandtab
