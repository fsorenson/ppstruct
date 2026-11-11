#!/usr/bin/python

from __future__ import print_function
from fs_lib import *

RPC_TASK_FLAGS_C = '''
#define RPC_TASK_ASYNC              0
#define RPC_TASK_SWAPPER            1
#define RPC_TASK_MOVEABLE           2
#define RPC_TASK_NULLCREDS          4
#define RPC_CALL_MAJORSEEN          5
#define RPC_TASK_NETUNREACH_FATAL   6
#define RPC_TASK_DYNAMIC            7
#define RPC_TASK_NO_ROUND_ROBIN     8
#define RPC_TASK_SOFT               9
#define RPC_TASK_SOFTCONN           10
#define RPC_TASK_SENT               11
#define RPC_TASK_TIMEOUT            12
#define RPC_TASK_NOCONNECT          13
#define RPC_TASK_NO_RETRANS_TIMEOUT 14
#define RPC_TASK_CRED_NOREF         15
'''
RPC_TASK_FLAGS = CDefine(RPC_TASK_FLAGS_C)

RPC_TASK_RUNSTATE_C = '''
#define RPC_TASK_RUNNING            0
#define RPC_TASK_QUEUED             1
#define RPC_TASK_ACTIVE             2
#define RPC_TASK_NEED_XMIT          3
#define RPC_TASK_NEED_RECV          4
#define RPC_TASK_MSG_PIN_WAIT       5
#define RPC_TASK_SIGNALLED          6
'''
RPC_TASK_RUNSTATE = CDefine(RPC_TASK_RUNSTATE_C)

RPC_PRIORITIES = {
	0: "LOW",
	1: "NORMAL",
	2: "HIGH",
	3: "PRIVILEGED",
}


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


@struct_label_string(("tk_pid",))
@struct_printer
def pp_struct_rpc_task(task, rlvl, ilvl):
	task = readSU("struct rpc_task", task)

	if task.hasField("tk_pid"):
		print("{}.tk_pid = {}".format(indent_str(ilvl), task.tk_pid))

	if task.hasField("tk_status"):
		print("{}.tk_status = {}".format(indent_str(ilvl), task.tk_status))

	if task.hasField("tk_rpc_status"):
		print("{}.tk_rpc_status = {}".format(indent_str(ilvl), task.tk_rpc_status))

	if task.hasField("tk_flags"):
		try:
			fl = int(task.tk_flags)
			fl_str = flags_to_string(fl, RPC_TASK_FLAGS)
			print("{}.tk_flags = 0x{:04x} - {}".format(indent_str(ilvl), fl, fl_str))
		except:
			pass

	if task.hasField("tk_runstate"):
		try:
			rs = int(task.tk_runstate)
			rs_str = flags_to_string(rs, RPC_TASK_RUNSTATE)
			print("{}.tk_runstate = 0x{:x} - {}".format(indent_str(ilvl), rs, rs_str))
		except:
			pass

	if task.hasField("tk_priority"):
		try:
			prio = int(task.tk_priority)
			prio_name = RPC_PRIORITIES.get(prio, "unknown")
			print("{}.tk_priority = {} ({})".format(indent_str(ilvl), prio, prio_name))
		except:
			pass

	if task.hasField("tk_owner") and task.tk_owner:
		print("{}.tk_owner = {}".format(indent_str(ilvl), task.tk_owner))

	if task.hasField("tk_count"):
		try:
			cnt = int(task.tk_count.counter)
			print("{}.tk_count = {}".format(indent_str(ilvl), cnt))
		except:
			pass

	if task.hasField("tk_action") and task.tk_action:
		act_addr = long(task.tk_action)
		act_sym = addr2sym(act_addr)
		act_str = " <{}>".format(act_sym) if act_sym else ""
		print("{}.tk_action = 0x{:x}{}".format(indent_str(ilvl), act_addr, act_str))

	if task.hasField("tk_callback") and task.tk_callback:
		cb_addr = long(task.tk_callback)
		cb_sym = addr2sym(cb_addr)
		cb_str = " <{}>".format(cb_sym) if cb_sym else ""
		print("{}.tk_callback = 0x{:x}{}".format(indent_str(ilvl), cb_addr, cb_str))

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
			print("{}.tk_ops(struct rpc_call_ops *)0x{:x}{}".format(indent_str(ilvl), long(task.tk_ops), ops_desc))
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

	if task.hasField("tk_waitqueue") and task.tk_waitqueue and not is_err_or_null(task.tk_waitqueue):
		wq_val = long(task.tk_waitqueue)
		wq_name = rpc_waitqueue_name(task, wq_val)
		wq_info = " ({})".format(wq_name) if wq_name else ""
		try:
			wq = readSU("struct rpc_wait_queue", wq_val)
			wq_info += " [qlen={}]".format(wq.qlen)
		except:
			pass
		print("{}.tk_waitqueue(struct rpc_wait_queue *)0x{:x}{}".format(indent_str(ilvl), wq_val, wq_info))

	if task.hasField("tk_workqueue") and task.tk_workqueue and not is_err_or_null(task.tk_workqueue):
		try:
			wq = readSU("struct workqueue_struct", task.tk_workqueue)
			print("{}.tk_workqueue = '{}' ((struct workqueue_struct *)0x{:x})".format(
				indent_str(ilvl), wq.name, long(task.tk_workqueue)))
		except:
			print("{}.tk_workqueue = (struct workqueue_struct *)0x{:x}".format(
				indent_str(ilvl), long(task.tk_workqueue)))

	if task.hasField("tk_timeout") and task.tk_timeout:
		print("{}.tk_timeout = {}".format(indent_str(ilvl), task.tk_timeout))

	if task.hasField("tk_timeouts") and task.tk_timeouts:
		print("{}.tk_timeouts = {}".format(indent_str(ilvl), task.tk_timeouts))

	if task.hasField("tk_start"):
		try:
			t_ns = int(task.tk_start)
			print("{}.tk_start = {} ns".format(indent_str(ilvl), t_ns))
		except:
			pass

	if task.hasField("tk_garb_retry") and task.tk_garb_retry:
		print("{}.tk_garb_retry = {}".format(indent_str(ilvl), task.tk_garb_retry))

	if task.hasField("tk_cred_retry") and task.tk_cred_retry:
		print("{}.tk_cred_retry = {}".format(indent_str(ilvl), task.tk_cred_retry))

	pp_struct_member(task, "tk_client", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(task, "tk_xprt", rlvl=rlvl, ilvl=ilvl)
	pp_struct_member(task, "tk_rqstp", rlvl=rlvl, ilvl=ilvl)


if __name__ == "__main__":
	program_display_struct(pp_struct_rpc_task)

# vim: sw=4 ts=4 noexpandtab
