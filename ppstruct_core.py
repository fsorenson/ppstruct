#!/usr/bin/python
from __future__ import print_function
import sys
import inspect
import traceback
import importlib
from functools import wraps, partial

from pykdump.API import *
from pp_utils import *

DEFAULT_RLVL = 3
pp_import_strings = [ "", "struct_", "fs.", "fs.struct_", "ppstruct_types.", "net.", "misc.", "fs.xfs." ]

def ppstruct_get_pp_struct_func(struct_type):
	pp_func_name = "pp_struct_{}".format(struct_type)
	known = globals().copy()
	known.update(locals())

	method = known.get(pp_func_name)
	if method:
		return method

	for prefix in pp_import_strings:
		imp = "{}{}".format(prefix, struct_type)

		try:
			mod = importlib.import_module(imp)
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
		return 0
	else:
		print("{} - not implemented".format(fmt_struct_addr(type, addr)))
		return -1

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
		if type(member_obj) == type(0):
			print("{}.{} - {}".format(indent_str(ilvl), member_name, member_obj))
			return
		else:
			print(" not sure what '{}.{}' type '{}' is".format(addr.PYT_symbol[7:], member_name, type(member_obj)))
			return
	if sym.startswith('struct '):
		member_type = sym[7:]
	else:
		member_type = sym

	print("{}.{} ".format(indent_str(ilvl), member_name), end="")
	pp_struct(member_type, member_addr, rlvl, ilvl)

def struct_label_string_quiet_fail(func):
	@wraps(func)
	def print_label_quiet_fail(*args, **kwargs):
		func(*args, label_quiet_fail=True, **kwargs)
	return print_label_quiet_fail

def struct_label_string(label_field):
	def struct_label_decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
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
				pass
	return struct_printer_decorator

def call_foreach_argv(func):
	for arg in sys.argv:
		addr = get_arg_value(arg)
		if addr != 0:
			func(addr, rlvl=DEFAULT_RLVL)

def program_display_struct(struct_func):
	call_foreach_argv(struct_func)

# vim: sw=4 ts=4 noexpandtab
