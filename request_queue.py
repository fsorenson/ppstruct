#!/usr/bin/python

from __future__ import print_function

from fs_lib import *


@struct_printer
def pp_struct_request_queue(rq, rlvl, ilvl):
	if rq.hasField("in_flight"):
		print("{ind}.in_flight = [ reads: {r}, writes: {w} ]".format(ind=indent_str(ilvl), r=rq.in_flight[0], w=rq.in_flight[1]))
	else:
		qd = rq.queue_depth if rq.hasField("queue_depth") else "?"
		nr = rq.nr_requests if rq.hasField("nr_requests") else "?"
		hw = rq.nr_hw_queues if rq.hasField("nr_hw_queues") else "?"
		print("{ind}.nr_requests = {nr}, .queue_depth = {qd}, .nr_hw_queues = {hw}".format(ind=indent_str(ilvl), nr=nr, qd=qd, hw=hw))

	if rq.hasField("limits"):
		lim = rq.limits
		print("{ind}.limits: logical_block_size = {lbs}, physical_block_size = {pbs}".format(ind=indent_str(ilvl), lbs=lim.logical_block_size, pbs=lim.physical_block_size))

	pp_struct_member(rq, "elevator", rlvl=rlvl, ilvl=ilvl)
	if rq.hasField("rq"):
		pp_struct_member(rq, "rq", rlvl=rlvl, ilvl=ilvl)
	if rq.hasField("backing_dev_info"):
		pp_struct_member(rq, "backing_dev_info", rlvl=rlvl, ilvl=ilvl)

	print("{}.queue_flags = 0x{:016x}".format(indent_str(ilvl), rq.queue_flags))

	if rq.hasField("queuedata") and rq.queuedata:
		pp_struct("scsi_device", rq.queuedata, rlvl=rlvl, ilvl=ilvl)


if __name__ == "__main__":
	program_display_struct(pp_struct_request_queue)

# vim: sw=4 ts=4 noexpandtab
