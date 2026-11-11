#!/usr/bin/python

from __future__ import print_function
from fs_lib import *
from LinuxDump.percpu import percpu_counter_sum

WB_STATE_C = '''
#define WB_registered           0
#define WB_writeback_running    1
#define WB_writeback            1
#define WB_has_dirty_io         2
#define WB_start_all            3
#define WB_start_dontcache      4
'''
WB_STATE = CDefine(WB_STATE_C)

@struct_printer
def pp_struct_bdi_writeback(wb, rlvl, ilvl):
	if wb.hasField("state"):
		state_val = int(wb.state)
		print("{}.state = 0x{s:x} - {str}".format(
			indent_str(ilvl), s=state_val, str=flags_to_string(state_val, WB_STATE)))

	if wb.hasField("writeback_inodes"):
		try:
			inodes = int(wb.writeback_inodes.counter)
			if inodes != 0:
				print("{}.writeback_inodes = {}".format(indent_str(ilvl), inodes))
		except:
			pass

	if wb.hasField("write_bandwidth"):
		bw_pages = int(wb.write_bandwidth)
		bw_bytes = bw_pages * 4096
		print("{}.write_bandwidth = {} ({}/s)".format(
			indent_str(ilvl), bw_pages, val_to_units_string(bw_bytes, 1024)))

	if wb.hasField("avg_write_bandwidth"):
		bw_pages = int(wb.avg_write_bandwidth)
		bw_bytes = bw_pages * 4096
		print("{}.avg_write_bandwidth = {} ({}/s)".format(
			indent_str(ilvl), bw_pages, val_to_units_string(bw_bytes, 1024)))

	if wb.hasField("dirty_ratelimit"):
		rl_pages = int(wb.dirty_ratelimit)
		rl_bytes = rl_pages * 4096
		print("{}.dirty_ratelimit = {} ({}/s)".format(
			indent_str(ilvl), rl_pages, val_to_units_string(rl_bytes, 1024)))

	if wb.hasField("balanced_dirty_ratelimit"):
		rl_pages = int(wb.balanced_dirty_ratelimit)
		rl_bytes = rl_pages * 4096
		print("{}.balanced_dirty_ratelimit = {} ({}/s)".format(
			indent_str(ilvl), rl_pages, val_to_units_string(rl_bytes, 1024)))

	if wb.hasField("dirty_exceeded") and int(wb.dirty_exceeded) != 0:
		print("{}.dirty_exceeded = {}".format(indent_str(ilvl), int(wb.dirty_exceeded)))

	if wb.hasField("stat"):
		try:
			wb_stat_item = EnumInfo("enum wb_stat_item")
			has_non_zero = False
			for i in range(0, wb_stat_item.NR_WB_STAT_ITEMS):
				try:
					val = percpu_counter_sum(wb.stat[i])
					if val != 0:
						if not has_non_zero:
							print("{}.stat:".format(indent_str(ilvl)))
							has_non_zero = True
						print("{}[{}]: {}".format(indent_str(ilvl+1), wb_stat_item.getnam(i), val))
				except:
					pass
		except:
			pass

if __name__ == "__main__":
	program_display_struct(pp_struct_bdi_writeback)

# vim: sw=4 ts=4 noexpandtab
