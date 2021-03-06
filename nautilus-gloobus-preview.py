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

import nautilus
import gobject
import subprocess
import urllib
import gtk
import os
# i18n
import gettext

try:
	gettext.install('nautilus-gloobus-preview', unicode=1)
	gettext.textdomain('nautilus-gloobus-preview')
except:
	pass

_ = gettext.gettext

# Key mask
from gp_hotkey.libkeymask import *


def run_cmd(cmd):
	"""
	Run shell commands, cmd have to be like ['executable','arg1','arg2', so on..]
	Directly print only errors, redirecting stdout (gloobus is too much verbose for myself)
	"""
	
	# Run cmd, redirecting stdout
	fnull = open(os.devnull, "w")
	subprocess.Popen(cmd,stdout=fnull)
	fnull.close()

class GloobusPreviewExtension(nautilus.MenuProvider):
	
	VER = '0.1.0'
	APP = 'nautilus-gloobus-preview'
	MSG_BASE = '['+APP+']'
	CURRENT_FILE = ''
	CURRENT_WINDOW = None
	USER_FILE = ''
	USER_MOD = []
	USER_KEY = gtk.gdk.keyval_from_name('space')
	
	def get_saved_hotkey(self):
		"""
		Load stored hotkey from user, fallback to default (space) if not found
		"""
		
		self.USER_FILE = os.path.expanduser('~/.config/nautilus-gloobus-preview/hotkey.cfg')
		# Check if file exists
		if not os.path.exists(self.USER_FILE):
			MSG = self.MSG_BASE + _('User\'s keybind not found at %s, reverting to \'space\'') % self.USER_FILE
			print MSG
			return False
		# Open file and reading string
		try:
			f = open(self.USER_FILE,'r')
			accel_string = f.read()
			f.close()
		except Exception:
			MSG = self.MSG_BASE + _('Error in user\'s file %s') % self.USER_FILE
			print MSG
			return False
		# Validate string
		if not is_accel_string_valid(accel_string):
			MSG = self.MSG_BASE + _('User\'s file %s not valid') % self.USER_FILE
			print MSG
			return False
		# Setting up variables
		self.USER_MOD = get_mod_list_from_accel_string(accel_string)
		self.USER_KEY = gtk.gdk.keyval_from_name(get_key_from_accel_string(accel_string))
		return True

	def can_preview(self, widget):
		"""
		Check if i'm on an Icon (and not editing it)
		"""
		
		#Current object with focus on window
		wdg_focus = widget.get_focus().get_name()
		#Parent of object above
		wdg_view = widget.get_focus().get_parent().get_name()
		#Icon & Compact view
		iconview = ((wdg_focus == 'FMIconContainer') and (wdg_view == 'FMIconView'))
		#Tree view
		treeview = ((wdg_focus == 'GtkTreeView') and (wdg_view == 'FMListView'))
		#Desktop view
		deskview = ((wdg_focus == 'FMIconContainer') and (wdg_view == 'FMDesktopIconView'))
		return (iconview or treeview or deskview)
	
	def on_key_press_event(self, widget, event):
		
		#Check if key pressed is my hotkey
		if (get_mod_list_from_event(event) == self.USER_MOD) & (event.keyval == self.USER_KEY):
			#Check if i'm on an Icon (and not editing it)
			if self.can_preview(widget):
				#Blocking default space Action (Open File)
				widget.emit_stop_by_name('key_press_event')
				#Call Gloobus for preview				
				if self.CURRENT_FILE != '':
					run_cmd(['gloobus-preview',self.CURRENT_FILE])
	
	def __init__(self):
		MSG = _('Initializing %s extension') % self.APP
		print MSG
		self.get_saved_hotkey()
		
		
	
	def menu_activate_cb(self, menu, file):
		"""
		Action for menus' item
		"""
		
		if file.is_gone():
			return
		#Launch gloobus-preview
		run_cmd(['gloobus-preview',self.CURRENT_FILE])

	def setup_key_event(self, window):
		#Bind key_event to current window
		window.connect('key_press_event', self.on_key_press_event)
	
	def get_toolbar_items(self, window, file):
		"""
		Invoked on window change , directory change
		"""
		
		# Do not set up key event if already
		if self.CURRENT_WINDOW != window:
			try:
				self.setup_key_event(window)
				self.CURRENT_WINDOW = window
				self.CURRENT_FILE = ''
			except Exception:
				MSG = self.MSG_BASE + _('Ignoring:')
				print MSG, window, type(window).__name__
				pass
	
	def get_file_items(self, window, files):
		"""
		Invoked on file selection, and other file actions
		"""
		
		# If get_toolbar fails, backup is needed
		if self.CURRENT_WINDOW != window:
			try:
				self.setup_key_event(window)
				self.CURRENT_WINDOW = window
			except Exception:
				MSG = self.MSG_BASE + _('Ignoring:')
				print MSG, window, type(window).__name__
				pass
		
		#Set CURRENT_FILE to void if selected file are 0 or more than 1
		if len(files) != 1:
			self.CURRENT_FILE = ''
			return
		file = files[0]
		self.CURRENT_FILE = urllib.unquote(file.get_uri()[7:])
		
		#Create Menu Item
		item = nautilus.MenuItem(
			'GloobusExtension::Preview_File',
			_('Preview'),
			_('Open a preview of selected file'),
			'gloobus-preview'
		)
		#Connecting signal to menu item
		item.connect('activate', self.menu_activate_cb, file)
		return [item]
