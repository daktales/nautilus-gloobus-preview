# -*- coding: UTF-8 -*-

# This file is part of Nautilus Gloobus Preview Extension

# Copyright (c) 2010-2011 - Walter Da Col <walter.dacol@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk

# List of possible modifier
MOD_LIST = [gtk.gdk.SHIFT_MASK, gtk.gdk.CONTROL_MASK, gtk.gdk.SUPER_MASK, gtk.gdk.MOD1_MASK]

# What I mean for:
# mod_list = list of modifier mask
# mod_mask = a gtk.gdk.<modifier>_Mask  

def get_mod_list_from_event(event):
	"""
	Get a mod_mask list from event state
	"""
	tmp_list = []
	tmp_state = event.state
	for mod_mask in MOD_LIST:
		#If accel is in event state
		if tmp_state & mod_mask:
			tmp_list.append(mod_mask)
	return tmp_list

def get_mod_name_from_mod_mask(mod_mask):
	"""
	Return human-readable string for mod_mask
	"""
	if mod_mask == None:
		return None
	if mod_mask & gtk.gdk.SHIFT_MASK: return "SHIFT"
	if mod_mask & gtk.gdk.CONTROL_MASK: return "CTRL"
	if mod_mask & gtk.gdk.SUPER_MASK: return "SUPER"
	if mod_mask & gtk.gdk.MOD1_MASK: return "ALT"
	return None

def get_mod_mask_from_name(mod_name):
	"""
	Return a mod_mask from name
	"""
	if mod_name == "SHIFT": return gtk.gdk.SHIFT_MASK
	if mod_name == "CTRL": return gtk.gdk.CONTROL_MASK
	if mod_name == "SUPER": return gtk.gdk.SUPER_MASK
	if mod_name == "ALT": return gtk.gdk.MOD1_MASK
	return None

def get_string_from_mod_list(mod_list):
	"""
	Return a string formed by MOD_NAME + OTHER_MOD_NAME + ...
	"""
	tmp_string =""
	for mod_mask in mod_list:
		tmp_string += get_mod_name_from_mod_mask(mod_mask)+" + "
	return tmp_string

def get_mod_list_from_accel_string(accel_string):
	"""
	Return modifier mask list from string
	"""
	tmp_list = accel_string.split(' + ')
	tmp_mod_list = []
	for idx in range(len(tmp_list)-1):
		tmp_mod_list.append(get_mod_mask_from_name(tmp_list[idx]))
	return tmp_mod_list
		
def get_key_from_accel_string(accel_string):
	"""
	Return key from string
	"""
	tmp_list = accel_string.split(' + ')
	tmp_key = tmp_list[len(tmp_list)-1]
	# keyval 0 is a not valid key
	if gtk.gdk.keyval_from_name(tmp_key) == 0:
		return ''
	return tmp_key

def is_accel_string_valid(accel_string):
	"""
	Validate accel string
	"""
	tmp_mod_list = get_mod_list_from_accel_string(accel_string)
	for item in tmp_mod_list:
		if get_mod_name_from_mod_mask(item) == None:
			return False
	if get_key_from_accel_string(accel_string) == '':
		return False
	return True
