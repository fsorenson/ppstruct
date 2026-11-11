#!/usr/bin/python

from __future__ import print_function
from fs_lib import *

@struct_label_string("name")
@struct_printer
def pp_struct_device_driver(driver, rlvl, ilvl):
	if driver.hasField("mod_name") and driver.mod_name and long(driver.mod_name) != 0:
		try:
			print("{}.mod_name: {}".format(indent_str(ilvl), driver.mod_name))
		except:
			pass

	if driver.hasField("bus") and driver.bus and long(driver.bus) != 0:
		try:
			print("{}.bus: {} (struct bus_type *)0x{:x}".format(indent_str(ilvl), driver.bus.name, long(driver.bus)))
		except:
			pass

if __name__ == "__main__":
	program_display_struct(pp_struct_device_driver)

# vim: sw=4 ts=4 noexpandtab
