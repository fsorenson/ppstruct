#!/usr/bin/python
from __future__ import print_function
import argparse
import re
import string
import sys
import inspect
import socket
import struct

from pykdump.API import *
from LinuxDump.Tasks import TaskTable
from LinuxDump.fs.dcache import *
from functools import wraps, partial

pp_import_strings = [ "", "struct_", "fs.", "fs.struct_", "ppstruct_types.", "net.", "misc.", "fs.xfs." ]

DEFAULT_RLVL = 3
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
#	if type(obj) == type(0) or type(obj) == type(0L):
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
#		if all(c in string.intdigits for c in arg): ### stupid python doesn't have string.intdigits?
		if all(c in '0123456789' for c in arg):
			return int(arg, 10)
		return int(arg, 16)
	except ValueError:
		return 0

def pp_time_ns(ns):
	s = int(ns / 1000000000)
#	ns %= 1000000000
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
#		crash> timespec
#	struct timespec {
#	    __kernel_time_t tv_sec;
#	    long tv_nsec;

#	crash> timespec64
#	struct timespec64 {
#	    time64_t tv_sec;
#	    long tv_nsec;

#		print("ts_in is {}".format(ts_in.PYT_symbol))
		if ts_in.PYT_symbol == "struct timespec" or ts_in.PYT_symbol == "struct timespec64":
#			print("found a timespec")
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
		import time
#		import datetime
#		from datetime import timedelta, time, date
#		from datetime import *
	except:
		print("no datetime?")
	try:
		lt = time.localtime(ts)
		return "{s}.{ss:09.0f} {tz}".format(s=time.strftime('%Y-%m-%d %H:%M:%S', lt), ss=(ts % 1) * 1000000000, tz=time.strftime('%Z', lt))
#		dt = datetime.data.fromtimestamp(ts)
#		return dt.isoformat()
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

	import math

#	print("unit strings: {}".format(unit_strings))

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
	str = "UNKNOWN"
	try:
		_S_enum_info = get_enum_info(enum_name)
		if _S_enum_info is None:
			return str
		try:
			_enum_key_list = sorted(_S_enum_info, key=lambda x: _S_enum_info[x])
			str = _enum_key_list[val]
		except: # no idea
			pass
	except:
		pass
	return str

def get_enum_bit_string(val, enum_name):
	str = "UNKNOWN"
	try:
		_S_enum_info = get_enum_info(enum_name)
		if _S_enum_info is None:
			return str
		try:
			_enum_key_list = sorted(_S_enum_info, key=lambda x: _S_enum_info[x])
			str = _enum_key_list[val.bit_length() - 1]
		except:
			pass
	except: # no idea
		pass
	return str

def print_enum_bit(val, enum_name):
	str = get_enum_bit_string(val, enum_name)
	print("{}".format(str))
	return str

def pp_enum_string(val, enum_name):
	str = get_enum_string(val, enum_name)
	print("{}".format(str))
	return str

def get_enum_tag_value(tag, enum_name):
	_S_enum_info = get_enum_info(enum_name)
	if _S_enum_info is None:
		return None
	try:
		_enum_key_list = sorted(_S_enum_info, key=lambda x: _S_enum_info[x])
		for k in _enum_key_list:
#			print("checking {} ({}) and {}".format(k, _S_enum_info[k], tag))
			if k == tag:
#				print("found that {} matches {}. returning {}".format(k, tag, _S_enum_info[k]))
				return _S_enum_info[k]
	except:
		print("exception in get_enum_tag_value")
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

# this func only half-baked
def obj__type(obj):
	try:
		sym = obj.PYT_symbol
	except AttributeError:
#		if type(obj) == type(0) or type(obj) == type(0L):
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
#		if type(obj) == type(0) or type(obj) == type(0L):
#			return None
		return None
	return None
def obj__class_type(obj):
	try:
		sym = obj.PYT_symbol
		if sym.startswith('class '):
			sym = sym[6:]
			return sym
	except AttributeError:
#		if type(obj) == type(0) or type(obj) == type(0L):
#			return None
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

def struct__has_member(str, mbr):
	return (member_size("struct " + str, mbr) != -1)

# lost where this was going... come back to it later, and see if I can remember
#def struct__member_obj(struct_obj, member):
#	try:
#		member_addr = struct__member_addr(struct_obj, member)
#
#		member_obj = addr_struct_obj(
#
#member_obj = struct__member_obj(addr, member_name)
#if member_obj == None:
#return
#
#	member_addr = long(member_obj)
#try:
#	sym = member_obj.PYT_symbol
#except AttributeError:
#	if type(member_obj) == type(0) or type(member_obj) == type(0L):
#		print("{ind}.{mbr} - {obj}".format(ind=indent_str(ilvl), mbr=member_name, obj=member_obj))
#		return
#	else: # no PYT_symbol...  now what?
#		print("not sure what '{sym}.{mbr}' type '{type}' is".format(sym=addr.PYT_symbol[7:], mbr=member_name, type=type(member_obj)))
#		return
#if sym.startswith('struct '):
#	member_type = sym[7:]




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
	member_obj = struct__member_addr(obj, member_name)
	if member_obj is None:
		return ""

	member_addr = long(member_obj)

	if member_obj == "long":
		return ".{name} = {val}".format(name=member_name, val=long(member_obj))

	try:
		sym = member_obj.PYT_symbol
	except:
		return " * %s *" % ret, member_obj.PYT_symbol
		return ""

	if sym == "kgid_t":
		ret = "kgid_t::: "
		return "ret:%s .%s = %d" % ret, member_name, struct_obj.val.gid_t
#			return ".%s = %d" % member_name, member_obj.val.gid_t
	if sym == "kuid_t":
		return "%s .%s = %d" % ret, member_name, member_obj.val.uid_t
	return "{ret}.{name} = {addr}".format(ret=ret, name=member_name, addr=long(member_obj))

# returns the pp_struct function, or False
def ppstruct_get_pp_struct_func(struct_type):
	pp_func_name = "pp_struct_{}".format(struct_type)
	known = globals().copy()
	known.update(locals())
#	print("**trying to find function {}".format(pp_func_name))

	method = known.get(pp_func_name)
	if method:
#		print("found known method to print {}".format(pp_func_name))
		return method
#	printDict(known)

#	print("looking for method to print {}".format(pp_func_name))

	if 1:
		try:
			import importlib
		except Exception as err:
			print("Unable to import importlib: {}".format(err))
			return False


#	for str in ppstruct_vars.pp_import_strings:


	for prefix in pp_import_strings:
		imp = "{}{}".format(prefix, struct_type)

		try:
#			print("trying to import {}".format(imp))
			mod = importlib.import_module(imp)
#			print("may have succeeded?")
		except ModuleNotFoundError as e:
			if getattr(e, 'name', None) == imp or (prefix and getattr(e, 'name', None) == prefix.rstrip('.')):
				continue
			print("Exception {} trying to import {}: {}".format(type(e).__name__, imp, e))
			continue
		except Exception as e:
			print("Exception {} trying to import {}: {}".format(type(e).__name__, imp, e))
			print("\nexception in {}: {}\n{}".format(inspect.currentframe().f_code.co_name, e, sys.exc_info()[2]))
			traceback.print_tb(sys.exc_info()[2])
			print("")
			continue
		try:
			method = mod.__dict__.get(pp_func_name)
			if method:
				return method
		except Exception as e:
			print("exception looking for '{}': {}".format(pp_func_name, e))
			pass
	return False

def ppstruct_func_exists(struct_type):
	return ppstruct_get_pp_struct_func(struct_type)


class StructOpts(object):
	def __init__(self, **kwargs):
		self.counts = False
		self.recurse = DEFAULT_RLVL
		self.locks = False
		self.stats = False
		self.prune = True
		for k, v in kwargs.items():
			setattr(self, k, v)
	def __getitem__(self, item):
		return getattr(self, item)
	def __setitem__(self, item, value):
		setattr(self, item, value)
	def get(self, item, default=None):
		return getattr(self, item, default)

class PPStructVars(object):
	def __init__(self):
		self.pp_struct_opts = StructOpts()
		self.pp_struct_prune = {'list': {}}
		self.pp_import_strings = pp_import_strings
	def __getitem__(self, item):
		return getattr(self, item)
	def __setitem__(self, item, value):
		if item == 'pp_struct_opts' and hasattr(value, '__dict__') and not isinstance(value, dict):
			setattr(self, item, StructOpts(**vars(value)))
			return
		setattr(self, item, value)
	def get(self, item, default=None):
		return getattr(self, item, default)

ppstruct_vars = PPStructVars()

def init_ppstruct_vars():
	global ppstruct_vars
	if not isinstance(ppstruct_vars, PPStructVars):
		ppstruct_vars = PPStructVars()
	else:
		ppstruct_vars.pp_struct_prune['list'].clear()

def pp_struct(type, addr, rlvl=1, ilvl=0):
	global ppstruct_vars
	if not isinstance(ppstruct_vars, PPStructVars):
		init_ppstruct_vars()

	func = ppstruct_get_pp_struct_func(type)

	if not func == False:
		func(addr, rlvl=rlvl, ilvl=ilvl)
	else:
#		print("{}{} - not implemented".format(indent_str(ilvl), fmt_struct_addr(type, addr)))
		print(" {} - not implemented".format(fmt_struct_addr(type, addr)))

def pp_struct_old3(type, addr, rlvl=1, ilvl=0):
	pp_func_name = "pp_struct_%s" % type

	known = globals().copy()
	known.update(locals())
	method = known.get(pp_func_name)
	if method:
		try:
			method(addr, rlvl=rlvl, ilvl=ilvl)
			return
		except:
			print("Could not call '{}'".format(pp_func_name))
	try:
		import importlib
	except:
		print("Error: could not import importlib")
		return

	mod = None
	for str in pp_import_strings:
		imp = "{}{}".format(str, type)

		try:
			mod = importlib.import_module(imp)
		except:
			continue
		method = mod.__dict__[pp_func_name]
		if method:
				method(addr, rlvl=rlvl, ilvl=ilvl)
				return

	print("{} - not implemented".format(fmt_struct_addr(type, addr)))



def pp_struct_old2(type, addr, rlvl=1, ilvl=0):
	try:
		import importlib
	except:
		print("Error: could not import importlib")
		return

	mod = None
	pp_func_name = "pp_struct_%s" % type
	for str in pp_import_strings:
		imp = "{}{}".format(str, type)

		try:
			mod = importlib.import_module(imp)
			break
		except:
			continue
		method = mod.__dict__[pp_func_name]
		if method:
			try:
				method(addr, rlvl=rlvl, ilvl=ilvl)
				return
			except:
				print("Could not call '{}' from '{}'".format(pp_func_name, imp))
#		else:
#			print "
	print("{} - not implemented".format(fmt_struct_addr(type, addr)))


def pp_struct_member_format_simple(struct_obj, member_name):
	try:
		return ".{} = {}".format(member_name, struct_obj.Eval(member_name))
	except:
		return ".{} = <NONE>"


def pp_struct_member_type(struct_obj, member_name, member_type, rlvl=1, ilvl=0):
	member_obj = struct__member_obj(struct_obj, member_name)
	if member_obj != None:
		member_addr = long(member_obj)

		print("{}.{} -".format(indent_str(ilvl), member_name), end="")
		pp_struct(member_type, member_addr, rlvl=rlvl, ilvl=ilvl)

def pp_struct_member(addr, member_name, rlvl=1, ilvl=0):
	member_obj = struct__member_obj(addr, member_name)
	if member_obj == None:
		return

	member_addr = long(member_obj)
	try:
		sym = member_obj.PYT_symbol
	except AttributeError:
#		if type(member_obj) == type(0) or type(member_obj) == type(0L):
		if type(member_obj) == type(0):
			print("{}.{} - {}".format(indent_str(ilvl), member_name, member_obj))
			return
		else: # no PYT_symbol...  now what?
			print(" not sure what '{}.{}' type '{}' is".format(addr.PYT_symbol[7:], member_name, type(member_obj)))
			return
	if sym.startswith('struct '):
		member_type = sym[7:]
#	elif sym.startswith("<class 'pykdump.lowlevel.StructResult_"):
	else:
		member_type = sym
#		print("{}.{} {} - not implemented".format(indent_str(ilvl), member_name, fmt_struct_addr(sym, addr)))
#		return
	if False:
		try:
			print("not sure how to display '{}.{}' type '{}' ({})".format(addr.PYT_symbol[7:], member_name, type(member_obj), sym))
#not sure how to display 'xfs_inode.i_df' type '<class 'pykdump.lowlevel.StructResult_xfs_ifork_t'>' (xfs_ifork_t)
#not sure how to display 'xfs_inode.i_df' type '<class 'pykdump.lowlevel.StructResult_xfs_ifork_t'>' (xfs_ifork_t)
		except Exception as e:
			print("exception on exception.  lucky us")
			exc_info = sys.exc_info()
			print("exception in {}: {}\n{}".format(inspect.currentframe().f_code.co_name, e, sys.exc_info()[2]))
			traceback.print_tb(sys.exc_info()[2])
			print("")
			pass
		return
#	if member_name == "i_mount":
#		print("***", end='')
	print("{}.{}".format(indent_str(ilvl), member_name), end="")
	pp_struct(member_type, member_addr, rlvl, ilvl)


def qstr(addr):
	try:
		q = readSU("struct qstr", long(addr))
		len = q.len
		return readmem(q.name, q.len)
	except:
#		print("hmm. some exception")
		pass


def struct_printer_ORIG(struct_name):
	def decorator(func):
		@wraps(func)
		def wrapper(addr, rlvl=1, ilvl=0):
			struct_name = func.__name__[10:]

			print("{}".format(fmt_struct_addr(struct_name, addr)))

			if addr != 0 and rlvl > 0:
				obj = addr_struct_obj(struct_name, addr)
				if obj != None:
					func(obj, rlvl-1, ilvl+1)
		return wrapper
	return decorator

def struct_label_string_quiet_fail(func):
	@wraps(func)
	def print_label_quiet_fail(*args, **kwargs):
		func(*args, label_quiet_fail=True, **kwargs)
	return print_label_quiet_fail

def struct_label_string(label_field):
	def struct_label_decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			struct_label_field = label_field
			func(*args, struct_label_field=label_field, **kwargs)
		return wrapper
	return struct_label_decorator

def print_oneline(func):
	@wraps(func)
	def print_oneline_wrapper(*args, **kwargs):
		func(*args, print_oneline=True, **kwargs)
	return print_oneline_wrapper

def print_no_NL(func):
	@wraps(func)
	def print_no_NL_wrapper(*args, **kwargs):
		func(*args, no_nl=True, **kwargs)
	return print_no_NL_wrapper

def never_prune(func):
	@wraps(func)
	def never_prune_wrapper(*args, **kwargs):
		func(*args, never_prune=True, **kwargs)
	return never_prune_wrapper

def requires_rlvl(req):
	def requires_rlvl_decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			func(*args, requires_rlvl=req, **kwargs)
		return wrapper
	return requires_rlvl_decorator

def no_rlvl(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		func(*args, requires_rlvl=0, **kwargs)
	return wrapper

def nonrecursive(func):
	@wraps(func)
	def nonrecursive_wrapper(*args, **kwargs):
		func(*args, requires_rlvl=0, **kwargs)
	return nonrecursive_wrapper

def struct_printer(func):
	@wraps(func)
	def struct_printer_decorator(addr, rlvl=1, ilvl=0, \
			struct_label_field=None, label_quiet_fail=True, no_nl=False, print_oneline=False, never_prune=False, requires_rlvl=1):
		struct_name = func.__name__
		if struct_name.startswith("pp_struct_"):
			struct_name = struct_name[len("pp_struct_"):]
		prune_this = False

		if addr:
			obj = addr_struct_obj(struct_name, addr)

			prune_key = "{}.0x{:016x}".format(struct_name, addr)

			opts = ppstruct_vars.pp_struct_opts
			should_prune = opts.prune if hasattr(opts, 'prune') else opts.get('prune', True)

			if should_prune and not never_prune:
				prune_previous_rlvl = ppstruct_vars.pp_struct_prune.get('list', {}).get(prune_key, -1)
				if prune_previous_rlvl != -1 and rlvl <= prune_previous_rlvl:
					prune_this = True
				else:
					ppstruct_vars.pp_struct_prune['list'][prune_key] = max(rlvl, prune_previous_rlvl)
		else: obj = None

		print("{}".format(fmt_struct_addr(struct_name, addr)), end="")

		if struct_label_field != None and obj != None:
			if isinstance(struct_label_field, (list, tuple)):
				label_fields = struct_label_field
			else:
				label_fields = [struct_label_field]
			found_label = False
			for lf in label_fields:
				try:
					if callable(lf):
						label = lf(obj)
					else:
						label = obj.Eval(lf)
					if label:
						ot = obj__type(label)
						if ot == 'struct' and obj__struct_type(label) == 'qstr':
							label = qstr(label).decode("utf-8")
						print(" - '{label}'".format(label=label), end="")
						found_label = True
						break
				except:
					pass
			if not found_label and not label_quiet_fail:
				print(" - '{label} unknown'".format(label=struct_label_field), end="")
		if prune_this:
			print(" ... [already displayed]")
		elif no_nl == False and print_oneline == False:
			print()

		if (obj != None) and (long(obj) != 0) and (rlvl - requires_rlvl >= 0) and (not prune_this):
			try:
				func(obj, rlvl=rlvl-requires_rlvl, ilvl=ilvl+1)
			except Exception as err:
				try:
					print("Exception occurred while printing {}: {}".format(struct_name, str(err)))
					print("{}, func.name='{}'".format(str(func), func.__name__))
					exc_info = sys.exc_info()
					print("exception in {}: {}\n{}".format(inspect.currentframe().f_code.co_name, err, sys.exc_info()[2]))
					traceback.print_tb(sys.exc_info()[2])
					print("")
				except Exception as e:
					print("exception on exception.  lucky us")
					exc_info = sys.exc_info()
					print("exception in {}: {}\n{}".format(inspect.currentframe().f_code.co_name, e, sys.exc_info()[2]))
					traceback.print_tb(sys.exc_info()[2])
					print("")


#				print("struct label 
				pass
	return struct_printer_decorator


def call_foreach_argv(func):
	for arg in sys.argv:
		addr = get_arg_value(arg)
		if addr != 0:
			func(addr, rlvl=DEFAULT_RLVL)

def program_display_struct(struct_func):
	call_foreach_argv(struct_func)


def printDict(di, fmt="{:25s}: {}"):
	for (key, val) in di.items():
		print(fmt.format(str(key), val))

def list_entry(tmp_addr, struct, member):
	try:
		addr = container_of(tmp_addr, "struct " + struct, member)
		return readSU("struct " + struct, addr)
	except:
		return None

##### probably need these to be at the bottom, after everything is defined
#import *
#from misc import *
#from fs import *
#from net import *

# vim: sw=4 ts=4 noexpandtab
