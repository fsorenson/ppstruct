#!/usr/bin/python

import sys, os

if __name__ == "__main__":
	mypath = os.path.dirname(os.path.realpath(sys.argv[0]))
	check_paths = [mypath, "/cores/crashext/epython/"]
	for p in check_paths:
		if os.path.isdir(p):
			if p not in sys.path:
				sys.path.append(p)

from fs_lib import *


def page__file_system_type_string(addr):
	try:
		from address_space import address_space__file_system_type_string
		page = addr_struct_obj("page", addr)
		return address_space__file_system_type_string(page.mapping)
	except Exception, err:
		return "Unknown in page: {}".format(str(err))

def get_pageflags(flags):
	flag_strings = []
	ret = ""

	_pageflags_mapping = {}
	try:
		_S_enum_info = EnumInfo("enum pageflags")
		print("enum_info = {}".format(_S_enum_info))

		list1 = []
		list2 = []
		found_split = 0
		for s in _S_enum_info:
			if s == '__NR_PAGEFLAGS':
				found_split = 1
			else:
				if not found_split:
					list1.append([s])
				else:
					list2.append([s])
#			found_split = 1 if s is '__NR_PAGEFLAGS'
#			else list1.append([s]) if not found_split
#			else list2.append([s])
#			if not found_split:
#				list1.append([s])
#			else:
#				list2.append([s])

		print("list1 = {}".format(list1))
		print("list2 = {}".format(list2))
		print("found_split = {}".format(found_split))

#_enum_mapping = { [_S_enum_info[s]] : s for s in _S_enum_info 
#_enum_mapping = { [_S_enum_info[s]] : s for s in _S_enum_info }

		info1 = [ s for s in _S_enum_info ]
		print("info1 = {}".format(info1))
#		info2 = { [_S_enum_info[s]] : s for s in _S_enum_info }
#		print("info2 = {}".format(info2))
#		info3 = { [_S_enum_info[s]] : s for s in _S_enum_info }
#		print("info3 = {}".format(info3))
#		info4 = { s for s in _S_enum_info }
#		print("info4 = {}".format(info4))

#		arry = 
#		elt0 = _S_enum_info[0]
#		print("element 0 = {}".format(elt0))

#		nr_pageflags = _S_enum_info["__NR_PAGEFLAGS"]
		print("here")
#		_pageflags_mapping = [ [_S_enum_info[s]] : s for s in _S_enum_info ]
#		_pageflags_mapping = { [_S_enum_info[s]] : s for s in _S_enum_info }
#		_pageflags_mapping = { [_S_enum_info[s]] : s for s in _S_enum_info[:nr_pageflags-1] }
#		_pageflags_mapping_high = { [_S_enum_info[s]] : s for s in _S_enum_info[nr_pageflags-1:] }
#
#		print("regular pageflags: {}".format(pageflags_mapping))
#		print("high word pageflags: {}".format(pageflags_mapping_high))

#		for bit in xrange(0, nr_pageflags - 0):
#			if (flags & (1 << bit)):
#				flag_strings.append(_pageflags_mapping[bit])

		ret = "|".join(str(s) for s in flag_strings)
#	except crash.error, AttributeError as e:
	except AttributeError as e:
		print("error in get_pageflags(): {}".format(e))
#		pass
	return ret


@struct_printer
def pp_struct_page(page, rlvl, ilvl):
	print("{}.index = {}".format(indent_str(ilvl), page.index))
	print("{}.flags = {}".format(indent_str(ilvl), get_pageflags(page.flags)))

	pp_struct_member(page, "mapping", rlvl=rlvl, ilvl=ilvl)

	print("{}page is type '{}'".format(indent_str(ilvl), page__file_system_type_string(long(page))))

	# hmm, too many variations


if __name__ == "__main__":
	program_display_struct(pp_struct_page)


# vim: sw=4 ts=4 noexpandtab
