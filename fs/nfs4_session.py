#!/usr/bin/python

from __future__ import print_function
from fs_lib import *

SESSION4_FLAGS_C = '''
#define SESSION4_PERSIST    0
#define SESSION4_BACK_CHAN  1
#define SESSION4_RDMA       2
'''
SESSION4_FLAGS = CDefine(SESSION4_FLAGS_C)

NFS4_SESSION_STATES_C = '''
#define NFS4_SESSION_INITING      0
#define NFS4_SESSION_ESTABLISHED  1
'''
NFS4_SESSION_STATES = CDefine(NFS4_SESSION_STATES_C)

NFS4_SLOT_TBL_STATES_C = '''
#define NFS4_SLOT_TBL_DRAINING    0
'''
NFS4_SLOT_TBL_STATES = CDefine(NFS4_SLOT_TBL_STATES_C)

def decode_sessionid(sess_id):
	try:
		raw = bytes([int(x) for x in sess_id.data])
		if len(raw) == 16:
			return "{:02x}{:02x}{:02x}{:02x}:{:02x}{:02x}{:02x}{:02x}:{:02x}{:02x}{:02x}{:02x}:{:02x}{:02x}{:02x}{:02x}".format(*raw)
	except:
		pass
	return ""

def format_slot_table_summary(tbl):
	used_slots = 0
	used_list = []
	if tbl.hasField("used_slots"):
		try:
			for idx, word in enumerate(tbl.used_slots):
				val = int(word)
				if val:
					for bit in range(64):
						if val & (1 << bit):
							slot_idx = idx * 64 + bit
							used_slots += 1
							if len(used_list) < 8:
								used_list.append(str(slot_idx))
		except:
			pass

	max_slots = int(tbl.max_slots) if tbl.hasField("max_slots") else 0

	highest_used_str = "none"
	if tbl.hasField("highest_used_slotid"):
		hu = int(tbl.highest_used_slotid)
		if hu != 0xffffffff and hu != 4294967295:
			highest_used_str = str(hu)

	target_highest = int(tbl.target_highest_slotid) if tbl.hasField("target_highest_slotid") else 0
	server_highest = int(tbl.server_highest_slotid) if tbl.hasField("server_highest_slotid") else 0

	state_str = "ACTIVE"
	if tbl.hasField("slot_tbl_state"):
		st = int(tbl.slot_tbl_state)
		if st != 0:
			state_str = flags_to_string(st, NFS4_SLOT_TBL_STATES)

	used_str = "{}/{}".format(used_slots, max_slots)
	if used_list:
		used_str += " [{}{}]".format(",".join(used_list), "..." if used_slots > len(used_list) else "")

	return "max_slots={}, used={}, highest_used={}, target_highest={}, server_highest={}, state={}".format(
		max_slots, used_str, highest_used_str, target_highest, server_highest, state_str)

@struct_label_string(("clp.cl_hostname",))
@struct_printer
def pp_struct_nfs4_session(ses, rlvl, ilvl):

	if ses.hasField("sess_id"):
		sid_str = decode_sessionid(ses.sess_id)
		if sid_str:
			print("{}.sess_id = {}".format(indent_str(ilvl), sid_str))

	if ses.hasField("flags") and ses.flags:
		try:
			fl = int(ses.flags)
			fl_str = flags_to_string(fl, SESSION4_FLAGS)
			print("{}.flags = 0x{:x} - {}".format(indent_str(ilvl), fl, fl_str))
		except:
			pass

	if ses.hasField("session_state") and ses.session_state:
		try:
			ss = int(ses.session_state)
			ss_str = flags_to_string(ss, NFS4_SESSION_STATES)
			print("{}.session_state = 0x{:x} - {}".format(indent_str(ilvl), ss, ss_str))
		except:
			pass

	if ses.hasField("hash_alg") and ses.hasField("ssv_len"):
		try:
			h_alg = int(ses.hash_alg)
			s_len = int(ses.ssv_len)
			if h_alg != 0 or s_len != 0:
				print("{}.ssv: hash_alg={}, ssv_len={}".format(indent_str(ilvl), h_alg, s_len))
		except:
			pass

	if ses.hasField("fc_attrs"):
		try:
			fc = ses.fc_attrs
			rq_sz = val_to_units_string(int(fc.max_rqst_sz), 1024)
			resp_sz = val_to_units_string(int(fc.max_resp_sz), 1024)
			print("{}.fc_attrs: max_rqst_sz={} ({}), max_resp_sz={} ({}), max_ops={}, max_reqs={}".format(
				indent_str(ilvl), int(fc.max_rqst_sz), rq_sz, int(fc.max_resp_sz), resp_sz, int(fc.max_ops), int(fc.max_reqs)))
		except:
			pass

	if ses.hasField("fc_slot_table"):
		try:
			st_desc = format_slot_table_summary(ses.fc_slot_table)
			print("{}.fc_slot_table: {}".format(indent_str(ilvl), st_desc))
		except:
			pass

	if ses.hasField("bc_attrs"):
		try:
			bc = ses.bc_attrs
			rq_sz = val_to_units_string(int(bc.max_rqst_sz), 1024)
			resp_sz = val_to_units_string(int(bc.max_resp_sz), 1024)
			print("{}.bc_attrs: max_rqst_sz={} ({}), max_resp_sz={} ({}), max_ops={}, max_reqs={}".format(
				indent_str(ilvl), int(bc.max_rqst_sz), rq_sz, int(bc.max_resp_sz), resp_sz, int(bc.max_ops), int(bc.max_reqs)))
		except:
			pass

	if ses.hasField("bc_slot_table"):
		try:
			st_desc = format_slot_table_summary(ses.bc_slot_table)
			print("{}.bc_slot_table: {}".format(indent_str(ilvl), st_desc))
		except:
			pass

	# Sub-structures
	if ses.hasField("clp") and not is_err_or_null(ses.clp):
		pp_struct_member(ses, "clp", rlvl=rlvl, ilvl=ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_nfs4_session)

# vim: sw=4 ts=4 noexpandtab
