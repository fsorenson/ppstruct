#!/usr/bin/python
from __future__ import print_function
from fs_lib import *

@struct_printer
def pp_struct_block_device(bdev, rlvl, ilvl):
	if bdev.hasField("bd_inode"):
		pp_struct_member(bdev, "bd_inode", rlvl=rlvl, ilvl=ilvl)
	if bdev.hasField("bd_mapping"):
		pp_struct_member(bdev, "bd_mapping", rlvl=rlvl, ilvl=ilvl)

	pp_struct_member(bdev, "bd_super", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(bdev, "bd_disk", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(bdev, "bd_queue", rlvl=rlvl, ilvl=ilvl)
	if bdev.hasField("bd_mutex"):
		pp_struct_member(bdev, "bd_mutex", rlvl=rlvl, ilvl=ilvl)

	# Block size
	if bdev.hasField("bd_block_size"):
		print("{}.bd_block_size = {}".format(indent_str(ilvl), bdev.bd_block_size))
	elif bdev.hasField("bd_queue") and bdev.bd_queue and bdev.bd_queue.hasField("limits"):
		print("{}.block_size: logical = {}, physical = {}".format(
			indent_str(ilvl), bdev.bd_queue.limits.logical_block_size, bdev.bd_queue.limits.physical_block_size))

	# Device capacity & in-flight stats
	if bdev.hasField("bd_nr_sectors"):
		nbytes = bdev.bd_nr_sectors * 512
		print("{}.bd_nr_sectors = {} ({})".format(
			indent_str(ilvl), bdev.bd_nr_sectors, val_to_units_string(nbytes, 1024)))

	if bdev.hasField("bd_stats") and bdev.bd_stats:
		try:
			stats = bdev.bd_stats
			def _inflight(x):
				if hasattr(x, 'hasField'):
					if x.hasField('a'):
						return int(x.a.counter)
					if x.hasField('counter'):
						return int(x.counter)
				return int(x)
			r_inflight = _inflight(stats.in_flight[0])
			w_inflight = _inflight(stats.in_flight[1])
			print("{}.in_flight = [ reads: {}, writes: {} ]".format(indent_str(ilvl), r_inflight, w_inflight))
		except:
			pass


if __name__ == "__main__":
	program_display_struct(pp_struct_block_device)

# vim: sw=4 ts=4 noexpandtab
