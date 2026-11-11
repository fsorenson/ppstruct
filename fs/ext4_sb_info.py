#!/usr/bin/python
from __future__ import print_function

from fs_lib import *
from LinuxDump import percpu
from LinuxDump.percpu import  percpu_counter_sum



def show_s_group_info(sgi, ilvl=0):
	print("{}sgi: {}".format(indent_str(ilvl), sgi))

	print("{}sgi[0]: {}".format(indent_str(ilvl), sgi[0]))
	print("{}sgi[0].bb_state: {}".format(indent_str(ilvl), sgi[0].bb_state))

	sgi = readSU("struct ext4_group_info (*)[]", sgi)

	print("{}sgi[0]: {}".format(indent_str(ilvl), sgi[0]))
	sgi0 = sgi[0]
	print("{}sgi0[0]: {}".format(indent_str(ilvl), sgi0[0]))

	sgi = readSU("struct ext4_group_info ***", sgi)
	print("{}sgi: {}".format(indent_str(ilvl), sgi))

def EXT4_DESC_PER_BLOCK(sbi):
	return sbi.s_desc_per_block

def EXT4_SB(sb):
	sb = readSU("struct super_block", sb)
	return readSU("struct ext4_sb_info", sb.s_fs_info)

def EXT4_DESC_SIZE(sbi):
#	return (EXT4_SB(sb).s_desc_size)
	return (sbi.s_desc_size)

def ext4_get_group_desc(sbi, block_group):
	print("looking for group_desc for block group {}".format(block_group))

	if block_group >= sbi.s_groups_count:
		printf("block_group ({}) is not >= sbi.s_groups_count ({})".format(block_group, sbi.s_groups_count))
		raise IndexError("ext4_error")

#	group_desc = block_group // EXT4_DESC_PER_BLOCK(sbi)
#	desc = block_group % EXT4_DESC_PER_BLOCK(sbi)

	group_desc = block_group >> EXT4_DESC_PER_BLOCK(sbi)
	offset = block_group & (EXT4_DESC_PER_BLOCK(sbi) - 1)

	if not sbi.s_group_desc[group_desc]:
		print("{}group descriptor not loaded - block_group: {}, group_desc: {}, desc: {}".format(
			indent_str(ilvl), block_group, group_desc, offset))
		raise IndexError("ext4_error")
		return None
	print("trying to get sbi.s_group_desc[{}] - p ((struct ext4_sb_info *)0x{:016x}).s_group_desc[{}]".format(group_desc, sbi, group_desc))
	try:
		print("sbi.s_group_desc: 0x{:016x}".format(sbi.s_group_desc))
		ael = sbi.s_group_desc[group_desc]
#print("block_group: {}, group_desc: {}, ael: {}, offset: {}".format(block_group, group_desc, repr(ael), offset))
	except:
		print("failed to get sbi.s_group_desc[{}] for ext4_sb_info 0x{:016x}".format(group_desc, sbi))

	print("{}ext4_sb_info.s_group_desc[{}] = 0x{:016x}".format(indent_str(ilvl), group_desc, ael))
	print("here")
	return None

	try:
		print("ael.b_data: 0x{:016x}".format(ael.b_data))
	except:
		print("could not get ael.b_data for ael 0x{:016x}".format(ael))
	try:
		addr = sbi.s_group_desc[group_desc].b_data + offset * EXT4_DESC_SIZE(sb)
		print("addr: 0x{:016x}".format(addr))
	except:
		print("couldn't calculate addr\n")
		return None
	try:
		desc = readSU("struct ext4_group_desc", sbi.s_group_desc[group_desc].b_data + offset * EXT4_DESC_SIZE(sb))
	except Exception as e:
		print("error trying to read ext4_group_desc at 0x{:016x}: {}".format(sbi.s_group_desc[group_desc].b_data, e))
	return desc
#	gdp = gdp.ptr
#
#	sz = struct_size("struct ext4_group_desc")
#	return readSU("struct ext4_group_desc", gdp + desc*sz)


def ext4_count_free_blocks(sbi, ilvl=0):
	desc_count = 0
	try:
		ngroups = sbi.s_groups_count
	except:
		print("could not get sbi.s_groups_count for ext4_sb_info 0x{:016x}".format(sbi))
		return

	print("{} group descriptor blocks for ext4_sb_info 0x{:016x}".format(ngroups, sbi))
	for i in range(ngroups):
		try:
			gd = ext4_get_group_desc(sbi, i)
			print("group descriptor {}: 0x{:016x}".format(i, gd))
		except:
			print("error getting ext4 group descriptor {}".format(i))
#			continue
			break
		try:
			desc_count += le16_to_cpu(gd.bg_free_blocks_count)
			continue
		except:
			print("error reading gd.bg_free_blocks_count")
			pass
	return desc_count

def ext4_blocks_count(es): # ext4_super_block
	return ((le32_to_cpu(es.s_blocks_count_hi) <<32) | le32_to_cpu(es.s_blocks_count_lo))
def ext4_r_blocks_count(es):
	return ((le32_to_cpu(es.s_r_blocks_count_hi) <<32) | le32_to_cpu(es.s_r_blocks_count_lo))

def EXT4_C2B(sbi, cluster):
	return ((cluster << sbi.s_cluster_bits))

@struct_printer
def pp_struct_ext4_sb_info(sbi, rlvl, ilvl):

	pp_struct_member(sbi, "s_es", rlvl=rlvl, ilvl=ilvl)

	s_groups_count = sbi.s_groups_count
	s_blocks_per_group = sbi.s_blocks_per_group
	s_blockfile_groups = sbi.s_blockfile_groups


	s_inodes_per_group = sbi.s_inodes_per_group
	s_inodes_per_block = sbi.s_inodes_per_block
	s_inode_size = sbi.s_inode_size



# and block size from the super_block
#s_groups_count = 8
#s_blocks_per_group = 0x8000 (32768)

	# try fudging the block size
	block_size = s_inodes_per_block * s_inode_size

	disk_size = block_size * s_blocks_per_group * s_groups_count
	size_str = val_to_units_string(disk_size, 1024)

	print("{}block size = {}".format(indent_str(ilvl), block_size))
	print("{}disk size = {} ({})".format(indent_str(ilvl), disk_size, size_str))

	s_es = sbi.s_es
	block_count = s_es.s_blocks_count_lo
	reserved_count = s_es.s_r_blocks_count_lo
	free_count = s_es.s_free_blocks_count_lo

	print("{}blocks: {} ({} - {})".format(indent_str(ilvl),
		block_count, block_count * block_size, val_to_units_string(block_count * block_size, 1024)))
	print("{}reserved blocks: {} ({} - {})".format(indent_str(ilvl),
		reserved_count, reserved_count * block_size, val_to_units_string(reserved_count * block_size, 1024)))
	print("{}free blocks: {} ({} - {})".format(indent_str(ilvl),
		free_count, free_count * block_size, val_to_units_string(free_count * block_size, 1024)))


#	print("need to atomic64_read(sb.s_resv_clusters)")
	resv_blocks = EXT4_C2B(sbi, sbi.s_resv_clusters.counter)
	print("resv_blocks: {}".format(resv_blocks))
	overhead = sbi.s_overhead
	print("overhead: {}".format(overhead))


	print("")
	print("ext4_blocks_count: {}".format(ext4_blocks_count(s_es)))
	print("EXT4_C2B(sbi, overhead): {}".format(EXT4_C2B(sbi, overhead)))
	f_blocks = ext4_blocks_count(s_es) - EXT4_C2B(sbi, overhead)

#	print("f_bfree = percpu_counter_sum_positive(&sbi->s_freeclusters_counter) - percpu_counter_sum_positive(&sbi->s_dirtyclusters_counter)");
#	print("sbi->s_freeclusters_counter: 0x{:016x}".format(sbi.s_freeclusters_counter))
	freeclusters_counter = percpu_counter_sum(sbi.s_freeclusters_counter)
#	print("  freeclusters_counter: {}".format(freeclusters_counter))
	dirtyclusters_counter = percpu_counter_sum(sbi.s_dirtyclusters_counter)
#	print("  dirtyclusters_counter: {}".format(dirtyclusters_counter))


	print("")
	print("f_blocks: {} ({})".format(f_blocks, val_to_units_string(f_blocks * block_size, 1024)))


	f_bfree = freeclusters_counter - dirtyclusters_counter
	if f_bfree < 0:
		f_bfree = 0
	f_bfree = EXT4_C2B(sbi, f_bfree)
	print("f_bfree: {} ({})".format(f_bfree, val_to_units_string(f_bfree * block_size, 1024)))

	f_bavail = f_bfree - (ext4_r_blocks_count(s_es) + resv_blocks)
	if f_bavail < 0:
		f_bavail = 0
	print("f_bavail: {} ({})".format(f_bavail, val_to_units_string(f_bavail * block_size, 1024)))



#	show_s_group_info(sbi.s_group_info, ilvl=ilvl+1)
#	show_ext4_group_info(sbi.s_group_info, ilvl=ilvl+1)


#disk size = 32768*8 * 1024


#s_groups_count = 0x8, 
#s_blockfile_groups = 0x8, 


#s_inode_size


#s_blocks_last

#s_resv_blocks
#reserved:
#	resuid
#	resgid

#percpu_counter:
#	s_freeblocks_counter
#	s_freeinodes_counter
#	s_dirs_counter
#	s_dirtyblocks_counter

#s_journal

#	pp_struct_member(sb, "s_type", rlvl=rlvl, ilvl=ilvl)

#	s_flags = sb.s_flags
#	print("{}.s_flags = 0x{:x} - {}".format(indent_str(ilvl), s_flags, flags_to_string(s_flags, SB_FLAGS)))

#	print("{}.s_blocksize = {}".format(indent_str(ilvl), sb.s_blocksize))
#	pp_struct_member(sb, "s_root", rlvl=rlvl, ilvl=ilvl)
#	pp_struct_member(sb, "s_bdev", rlvl=rlvl, ilvl=ilvl)
#	pp_struct_member(sb, "s_bdi", rlvl=rlvl, ilvl=ilvl)


#	if member_size("struct super_block", "s_files") != -1:
#		## works through 2.6.36, after which this became per-cpu
#		s_files_len = len(ListHead(sb.s_files))
#		print("{}.s_files: list -H 0x{:016x} ({} entries)".format(indent_str(ilvl), Addr(sb.s_files), s_files_len))
#	if member_size("struct super_block", "s_inodes") != -1:
#		s_inodes_len = len(ListHead(sb.s_inodes))
#		print("{}.s_inodes: list -H 0x{:016x} ({} entries}".format(indent_str(ilvl), Addr(sb.s_inodes), s_inodes_len))



if __name__ == "__main__":
	program_display_struct(pp_struct_ext4_sb_info)

# vim: sw=4 ts=4 noexpandtab
