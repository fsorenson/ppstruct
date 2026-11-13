#!/usr/bin/python

from __future__ import print_function
from fs_lib import *

RPC_TASK_FLAGS_C = '''
#define ASYNC              0
#define SWAPPER            1
#define MOVEABLE           2
#define NULLCREDS          4
#define MAJORSEEN          5
#define NETUNREACH_FATAL   6
#define DYNAMIC            7
#define NO_ROUND_ROBIN     8
#define SOFT               9
#define SOFTCONN           10
#define SENT               11
#define TIMEOUT            12
#define NOCONNECT          13
#define NO_RETRANS_TIMEOUT 14
#define CRED_NOREF         15
'''
RPC_TASK_FLAGS = CDefine(RPC_TASK_FLAGS_C)

RPC_TASK_RUNSTATE_C = '''
#define RUNNING            0
#define QUEUED             1
#define ACTIVE             2
#define NEED_XMIT          3
#define NEED_RECV          4
#define MSG_PIN_WAIT       5
#define SIGNALLED          6
'''
RPC_TASK_RUNSTATE = CDefine(RPC_TASK_RUNSTATE_C)

RPC_PRIORITIES = {
	0: "LOW",
	1: "NORMAL",
	2: "HIGH",
	3: "PRIVILEGED",
}


def format_elapsed_time(elapsed_ns):
	if elapsed_ns < 0:
		elapsed_ns = 0
	ns = elapsed_ns % 1000000000
	total_secs = elapsed_ns // 1000000000
	secs = total_secs % 60
	total_mins = total_secs // 60
	mins = total_mins % 60
	hours = total_mins // 60

	if hours > 0:
		return "{:d}:{:02d}:{:02d}.{:09d} ago".format(hours, mins, secs, ns)
	elif mins > 0:
		return "{:d}:{:02d}.{:09d} ago".format(mins, secs, ns)
	else:
		return "{:d}.{:09d} ago".format(secs, ns)


def get_current_time_ns():
	if symbol_exists("last_jiffies_update"):
		try:
			return int(readSymbol("last_jiffies_update"))
		except:
			pass
	if symbol_exists("jiffies_64"):
		try:
			j = int(readSymbol("jiffies_64"))
			hz = 1000
			if symbol_exists("CONFIG_HZ"):
				hz = int(readSymbol("CONFIG_HZ"))
			return int(j * (1000000000 / hz))
		except:
			pass
	return None


def rpc_waitqueue_name(task, wq_addr):
	if not wq_addr or is_err_or_null(wq_addr):
		return None
	wq_val = long(wq_addr)
	if task.hasField("tk_xprt") and task.tk_xprt and not is_err_or_null(task.tk_xprt):
		try:
			xprt = readSU("struct rpc_xprt", task.tk_xprt)
			if wq_val == long(xprt.binding):
				return "xprt->binding"
			elif wq_val == long(xprt.sending):
				return "xprt->sending"
			elif wq_val == long(xprt.pending):
				return "xprt->pending"
			elif wq_val == long(xprt.backlog):
				return "xprt->backlog"
		except:
			pass
	sym = addr2sym(wq_val)
	if sym:
		return sym
	return None


def rpc_task_label(task):
	if task.hasField("tk_rqstp") and task.tk_rqstp and not is_err_or_null(task.tk_rqstp):
		try:
			rq = readSU("struct rpc_rqst", task.tk_rqstp)
			return "0x{:08x}".format(int(rq.rq_xid))
		except:
			pass
	if task.hasField("tk_pid") and task.tk_pid:
		return "pid:{}".format(task.tk_pid)
	return None


@struct_label_string(rpc_task_label)
@struct_printer
def pp_struct_rpc_task(task, rlvl, ilvl):
	task = readSU("struct rpc_task", task)

	line1 = []
	if task.hasField("tk_status"):
		line1.append(".tk_status = {}".format(task.tk_status))
	if task.hasField("tk_rpc_status"):
		line1.append(".tk_rpc_status = {}".format(task.tk_rpc_status))
	if task.hasField("tk_owner") and task.tk_owner:
		line1.append(".tk_owner = {}".format(task.tk_owner))
	if task.hasField("tk_priority"):
		try:
			prio = int(task.tk_priority)
			prio_name = RPC_PRIORITIES.get(prio, "unknown")
			line1.append(".tk_priority = {} ({})".format(prio, prio_name))
		except:
			pass
	if task.hasField("tk_count"):
		try:
			opts = ppstruct_vars.pp_struct_opts
			show_counts = opts.counts if hasattr(opts, 'counts') else opts.get('counts', False)
			if show_counts:
				line1.append(".tk_count = {}".format(int(task.tk_count.counter)))
		except:
			pass
	if line1:
		print("{}{}".format(indent_str(ilvl), ", ".join(line1)))

	line2 = []
	if task.hasField("tk_flags"):
		try:
			fl = int(task.tk_flags)
			fl_str = flags_to_string(fl, RPC_TASK_FLAGS)
			line2.append(".tk_flags = 0x{:04x} - {}".format(fl, fl_str))
		except:
			pass
	if task.hasField("tk_runstate"):
		try:
			rs = int(task.tk_runstate)
			rs_str = flags_to_string(rs, RPC_TASK_RUNSTATE)
			line2.append(".tk_runstate = 0x{:x} - {}".format(rs, rs_str))
		except:
			pass
	if line2:
		print("{}{}".format(indent_str(ilvl), ", ".join(line2)))

	line3 = []
	if task.hasField("tk_timeout") and task.tk_timeout:
		line3.append(".tk_timeout = {}".format(task.tk_timeout))
	if task.hasField("tk_start"):
		try:
			now_ns = get_current_time_ns()
			if now_ns is not None:
				elapsed_ns = now_ns - int(task.tk_start)
				line3.append(".tk_start = {}".format(format_elapsed_time(elapsed_ns)))
			else:
				line3.append(".tk_start = {} ns".format(int(task.tk_start)))
		except:
			pass
	if task.hasField("tk_timeouts") and task.tk_timeouts:
		line3.append(".tk_timeouts = {}".format(task.tk_timeouts))
	if line3:
		print("{}{}".format(indent_str(ilvl), ", ".join(line3)))

	# Only display retries if non-default (< 2)
	retries = []
	if task.hasField("tk_garb_retry") and task.tk_garb_retry < 2:
		retries.append("garb={}".format(task.tk_garb_retry))
	if task.hasField("tk_cred_retry") and task.tk_cred_retry < 2:
		retries.append("cred={}".format(task.tk_cred_retry))
	if retries:
		print("{}.tk_retries: {}".format(indent_str(ilvl), ", ".join(retries)))

	line4 = []
	if task.hasField("tk_action") and task.tk_action:
		act_addr = long(task.tk_action)
		act_sym = addr2sym(act_addr)
		act_str = " <{}>".format(act_sym) if act_sym else ""
		line4.append(".tk_action = 0x{:x}{}".format(act_addr, act_str))
	if task.hasField("tk_callback") and task.tk_callback:
		cb_addr = long(task.tk_callback)
		cb_sym = addr2sym(cb_addr)
		cb_str = " <{}>".format(cb_sym) if cb_sym else ""
		line4.append(".tk_callback = 0x{:x}{}".format(cb_addr, cb_str))
	if line4:
		print("{}{}".format(indent_str(ilvl), ", ".join(line4)))

	if task.hasField("tk_ops") and task.tk_ops and not is_err_or_null(task.tk_ops):
		try:
			ops = readSU("struct rpc_call_ops", task.tk_ops)
			ops_parts = []
			if ops.rpc_call_prepare:
				sym = addr2sym(long(ops.rpc_call_prepare))
				ops_parts.append("prepare: {}".format(sym if sym else hex(long(ops.rpc_call_prepare))))
			if ops.rpc_call_done:
				sym = addr2sym(long(ops.rpc_call_done))
				ops_parts.append("done: {}".format(sym if sym else hex(long(ops.rpc_call_done))))
			if ops.rpc_release:
				sym = addr2sym(long(ops.rpc_release))
				ops_parts.append("release: {}".format(sym if sym else hex(long(ops.rpc_release))))
			ops_desc = " ({})".format(", ".join(ops_parts)) if ops_parts else ""
			print("{}.tk_ops (struct rpc_call_ops *)0x{:x}{}".format(indent_str(ilvl), long(task.tk_ops), ops_desc))
		except:
			pass

	if task.hasField("tk_calldata") and task.tk_calldata and not is_err_or_null(task.tk_calldata):
		calldata_addr = long(task.tk_calldata)
		calldata_sym = addr2sym(calldata_addr)
		calldata_str = " <{}>".format(calldata_sym) if calldata_sym else ""
		print("{}.tk_calldata = 0x{:x}{}".format(indent_str(ilvl), calldata_addr, calldata_str))

	if task.hasField("tk_msg"):
		try:
			msg = task.tk_msg
			proc_str = ""
			if msg.rpc_proc and not is_err_or_null(msg.rpc_proc):
				try:
					proc = readSU("struct rpc_procinfo", msg.rpc_proc)
					proc_str = "proc={}:'{}'".format(proc.p_proc, proc.p_name)
				except:
					proc_str = "proc=0x{:x}".format(long(msg.rpc_proc))
			msg_parts = []
			if proc_str:
				msg_parts.append(proc_str)
			if msg.rpc_argp and not is_err_or_null(msg.rpc_argp):
				msg_parts.append("argp=0x{:x}".format(long(msg.rpc_argp)))
			if msg.rpc_resp and not is_err_or_null(msg.rpc_resp):
				msg_parts.append("resp=0x{:x}".format(long(msg.rpc_resp)))
			if msg.rpc_cred and not is_err_or_null(msg.rpc_cred):
				msg_parts.append("cred=0x{:x}".format(long(msg.rpc_cred)))
			print("{}.tk_msg = {}".format(indent_str(ilvl), ", ".join(msg_parts)))
		except:
			pass

	line_wq = []
	if task.hasField("tk_waitqueue") and task.tk_waitqueue and not is_err_or_null(task.tk_waitqueue):
		wq_val = long(task.tk_waitqueue)
		wq_name = rpc_waitqueue_name(task, wq_val)
		wq_info = " ({})".format(wq_name) if wq_name else ""
		try:
			wq = readSU("struct rpc_wait_queue", wq_val)
			wq_info += " [qlen={}]".format(wq.qlen)
		except:
			pass
		line_wq.append(".tk_waitqueue (struct rpc_wait_queue *)0x{:x}{}".format(wq_val, wq_info))
	if task.hasField("tk_workqueue") and task.tk_workqueue and not is_err_or_null(task.tk_workqueue):
		try:
			wq = readSU("struct workqueue_struct", task.tk_workqueue)
			line_wq.append(".tk_workqueue = '{}'".format(wq.name))
		except:
			line_wq.append(".tk_workqueue = (struct workqueue_struct *)0x{:x}".format(long(task.tk_workqueue)))
	if line_wq:
		print("{}{}".format(indent_str(ilvl), ", ".join(line_wq)))

	pp_struct_member(task, "tk_client", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(task, "tk_xprt", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(task, "tk_rqstp", rlvl=rlvl, ilvl=ilvl)


if __name__ == "__main__":
	program_display_struct(pp_struct_rpc_task)

# vim: sw=4 ts=4 noexpandtab
