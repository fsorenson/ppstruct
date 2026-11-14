#!/usr/bin/python
from __future__ import print_function
import re
import string
import sys
import socket
import struct
import math
import time

from pykdump.API import *
from LinuxDump.Tasks import TaskTable
from LinuxDump.fs.dcache import *

PAGE_SIZE = 4096

def is_err_or_null(ptr):
	if not ptr:
		return True
	try:
		val = int(ptr)
		if val == 0 or val >= 0xfffffffffffff000 or (val < 0 and val >= -4095):
			return True
	except:
		pass
	return False

def get_err_code(ptr):
	try:
		val = int(ptr)
		if val >= 0xfffffffffffff000:
			return -(0x10000000000000000 - val)
		elif val < 0 and val >= -4095:
			return val
	except:
		pass
	return 0

def decode_sockaddr_storage(ksockaddr):
	try:
		family = int(ksockaddr.ss_family)
		data = ksockaddr.__data.ByteArray
		if family == socket.AF_INET:
			port = data[0] * 256 + data[1]
			ip = socket.inet_ntop(socket.AF_INET, struct.pack('4B', *data[2:6]))
			return "{}:{}".format(ip, port) if port else ip
		elif family == socket.AF_INET6:
			port = data[0] * 256 + data[1]
			ip = socket.inet_ntop(socket.AF_INET6, struct.pack('16B', *data[6:22]))
			return "[{}]:{}".format(ip, port) if port else ip
	except Exception:
		pass
	return None

def obj_is_inttype(obj):
	if type(obj) == type(0):
		return 1
	try:
		if type(obj) == type(0):
			return 1
	except:
		pass
	return 0

def obj_is_floattype(obj):
	return isinstance(obj, float)

def flags_to_string(flags, strings):
	result = []
	for name, val in strings.items():
		if flags & (1 << val) != 0:
			result.append(name)
	return "|".join(result)

def defines_to_string(match_val, strings):
	for name, val in strings.items():
		if match_val == val:
			return name
	return "UNKNOWN"

def get_arg_value(arg):
	try:
		if '.' in arg:
			return float(arg)
		if arg.lower().startswith('0x'):
			return int(arg, 16)
		if arg.startswith('0') and all(c in string.octdigits for c in arg):
			return int(arg, 8)
		if all(c in '0123456789' for c in arg):
			return int(arg, 10)
		return int(arg, 16)
	except ValueError:
		return 0

def pp_time_ns(ns):
	s = int(ns / 1000000000)
	ns = int(ns % 1000000000)
	m = int(s / 60)
	s %= 60
	h = int(m / 60)
	m %= 60
	d = int(h / 24)
	h %= 24
	return "%d %2d:%02d:%02d.%09d" % (d, h, m, s, ns)

def pp_time_us(us):
	return pp_time_ns(us * 1000)

def pp_time_ms(ms):
	return pp_time_ns(ms * 1000 * 1000)

def pp_time_s(s):
	return pp_time_ns(s * 1000 * 1000 * 1000)

def timespec_to_string(ts_in):
	ts = None
	try:
		if ts_in.PYT_symbol == "struct timespec" or ts_in.PYT_symbol == "struct timespec64":
			ts = ts_in.tv_sec + ts_in.tv_nsec / 1000000000.0
	except AttributeError:
		pass
	if obj_is_inttype(ts_in):
		ts = ts_in
	elif obj_is_floattype(ts_in):
		ts = ts_in
	if ts is None:
		return None
	try:
		lt = time.localtime(ts)
		return "{s}.{ss:09.0f} {tz}".format(s=time.strftime('%Y-%m-%d %H:%M:%S', lt), ss=(ts % 1) * 1000000000, tz=time.strftime('%Z', lt))
	except:
		return None

def indent_str(lvl):
	return "{spaces}".format(spaces = ' ' * 4 * lvl)

def indent(lvl):
	print(indent_str(lvl), end="")

def val_to_units_string(val, base, custom_strings=None):
	if custom_strings == None:
		if base == "SI":
			base = 1000
			unit_strings = [ "", "K", "M", "G", "T", "P", "E", "Z", "Y" ]
		elif base == 1000:
			unit_strings = [ "Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB" ]
		elif base == 1024:
			unit_strings = [ "Bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB" ]
		else:
			base = 1
	else:
		unit_strings = custom_strings

	if base == 1:
		return "{}".format(val)

	if val == 0:
		unit = unit_strings[0].strip()
		return "0 {}".format(unit) if unit else "0"

	negative = False
	if val < 0:
		negative = True
		val = -val

	i = int(math.floor(math.log(val, base)))
	if i >= len(unit_strings):
		return "-{}".format(val) if negative else "{}".format(val)

	divider = math.pow(base, i)
	unit = unit_strings[i].strip()
	val_divided = val / divider
	val_str = "{:.0f}".format(val_divided) if (int(val_divided) == val_divided) else "{:.2f}".format(val_divided)
	res = "{} {}".format(val_str, unit) if unit else val_str
	return "-{}".format(res) if negative else res

def get_enum_info(enum_name):
	try:
		_S_enum_info = EnumInfo("enum " + enum_name)
		return _S_enum_info
	except:
		return None

def get_enum_string(val, enum_name):
	str_val = "UNKNOWN"
	try:
		_S_enum_info = get_enum_info(enum_name)
		if _S_enum_info is None:
			return str_val
		try:
			_enum_key_list = sorted(_S_enum_info, key=lambda x: _S_enum_info[x])
			str_val = _enum_key_list[val]
		except:
			pass
	except:
		pass
	return str_val

def get_enum_bit_string(val, enum_name):
	str_val = "UNKNOWN"
	try:
		_S_enum_info = get_enum_info(enum_name)
		if _S_enum_info is None:
			return str_val
		try:
			_enum_key_list = sorted(_S_enum_info, key=lambda x: _S_enum_info[x])
			str_val = _enum_key_list[val.bit_length() - 1]
		except:
			pass
	except:
		pass
	return str_val

def print_enum_bit(val, enum_name):
	str_val = get_enum_bit_string(val, enum_name)
	print("{}".format(str_val))
	return str_val

def pp_enum_string(val, enum_name):
	str_val = get_enum_string(val, enum_name)
	print("{}".format(str_val))
	return str_val

def get_enum_tag_value(tag, enum_name):
	_S_enum_info = get_enum_info(enum_name)
	if _S_enum_info is None:
		return None
	try:
		_enum_key_list = sorted(_S_enum_info, key=lambda x: _S_enum_info[x])
		for k in _enum_key_list:
			if k == tag:
				return _S_enum_info[k]
	except:
		pass
	return None

def pp_uid(addr):
	try:
		sym = addr.PYT_symbol
	except:
		return ".uid = {uid}".format(uid=addr)

	if sym == 'kuid_t':
		return ".uid = {uid}".format(uid=addr.val)
	else:
		return ".uid = {uid}".format(uid=addr)

def pp_gid(addr):
	try:
		sym = addr.PYT_symbol
	except:
		return ".gid = {gid}".format(gid=addr)

	if sym == 'kgid_t':
		return ".gid = {gid}".format(gid=addr.val)
	else:
		return ".gid = {gid}".format(gid=addr)

def obj__type(obj):
	try:
		sym = obj.PYT_symbol
	except AttributeError:
		if type(obj) == type(0):
			return 'int'
		else:
			return "type '{}' is unknown".format(type(obj))
	if sym.startswith('struct '):
		return 'struct'
	if sym.startswith('class '):
		return 'class'

def obj__struct_type(obj):
	try:
		sym = obj.PYT_symbol
		if sym.startswith('struct '):
			sym = sym[7:]
			return sym
	except AttributeError:
		return None
	return None

def obj__class_type(obj):
	try:
		sym = obj.PYT_symbol
		if sym.startswith('class '):
			sym = sym[6:]
			return sym
	except AttributeError:
		return None
	return None

def struct__member_obj(struct_obj, member):
	try:
		if struct_obj.hasField(member):
			member_obj = struct_obj.Eval(member)
			return member_obj
	except:
		pass
	return None

def struct__has_member(str_name, mbr):
	return (member_size("struct " + str_name, mbr) != -1)

def addr_struct_obj(struct_name, addr):
	obj = None
	try:
		obj = readSU("struct " + struct_name, addr)
	except:
		print(" - unknown type 'struct {struct_name}'".format(struct_name = struct_name))
	return obj

def fmt_struct_addr(name, addr):
	return "(struct {name} *)0x{addr:016x}".format(name = name, addr = addr)

def struct__member_addr(obj, member_name):
	if obj.HasField(member_name):
		return obj.Eval(member_name)
	return 0

def pp_member_val(struct_obj, member_name):
	ret = ""
	member_obj = struct__member_addr(struct_obj, member_name)
	if member_obj is None:
		return ""

	member_addr = long(member_obj)

	if member_obj == "long":
		return ".{name} = {val}".format(name=member_name, val=long(member_obj))

	try:
		sym = member_obj.PYT_symbol
	except:
		return " * %s *" % ret, member_obj.PYT_symbol

	if sym == "kgid_t":
		ret = "kgid_t::: "
		return "ret:%s .%s = %d" % ret, member_name, struct_obj.val.gid_t
	if sym == "kuid_t":
		return "%s .%s = %d" % ret, member_name, member_obj.val.uid_t
	return "{ret}.{name} = {addr}".format(ret=ret, name=member_name, addr=long(member_obj))

def qstr(addr):
	try:
		q = readSU("struct qstr", long(addr))
		return readmem(q.name, q.len)
	except:
		pass

def printDict(di, fmt="{:25s}: {}"):
	for (key, val) in di.items():
		print(fmt.format(str(key), val))

def list_entry(tmp_addr, struct, member):
	try:
		addr = container_of(tmp_addr, "struct " + struct, member)
		return readSU("struct " + struct, addr)
	except:
		return None

# vim: sw=4 ts=4 noexpandtab
