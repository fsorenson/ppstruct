#!/usr/bin/python

from __future__ import print_function
from fs_lib import *

@struct_label_string(("init_name", "kobj.name"))
@struct_printer
def pp_struct_device(device, rlvl, ilvl):

	if device.hasField("devt") and device.devt:
		devt = int(device.devt)
		maj = devt >> 20
		min = devt & 0xfffff
		print("{}.devt: {}:{} (0x{:x})".format(indent_str(ilvl), maj, min, devt))

	if device.hasField("class"):
		dev_class = getattr(device, "class")
		if dev_class and long(dev_class) != 0:
			try:
				print("{}.class: {} (struct class *)0x{:x}".format(indent_str(ilvl), dev_class.name, long(dev_class)))
			except Exception:
				print("{}.class: (struct class *)0x{:x}".format(indent_str(ilvl), long(dev_class)))

	if device.hasField("type") and device.type and long(device.type) != 0:
		try:
			print("{}.type: {} (struct device_type *)0x{:x}".format(indent_str(ilvl), device.type.name, long(device.type)))
		except Exception:
			print("{}.type: (struct device_type *)0x{:x}".format(indent_str(ilvl), long(device.type)))

	if device.hasField("bus") and device.bus and long(device.bus) != 0:
		try:
			print("{}.bus: {} (struct bus_type *)0x{:x}".format(indent_str(ilvl), device.bus.name, long(device.bus)))
		except Exception:
			print("{}.bus: (struct bus_type *)0x{:x}".format(indent_str(ilvl), long(device.bus)))

	if device.hasField("driver") and device.driver and long(device.driver) != 0:
		pp_struct_member(device, "driver", rlvl, ilvl)

	if device.hasField("parent") and device.parent and long(device.parent) != 0:
		pp_struct_member(device, "parent", rlvl, ilvl)

if __name__ == "__main__":
	program_display_struct(pp_struct_device)

# vim: sw=4 ts=4 noexpandtab
