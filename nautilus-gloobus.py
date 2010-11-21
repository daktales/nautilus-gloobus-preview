# -*- coding: UTF-8 -*-

# This file is part of Nautilus Gloobus Preview Extension

# Copyright (c) 2009-2010 - Walter Da Col <walter.dacol@gmail.com>

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
import locale
import gtk
import os
# Localization
from gettext import gettext as _

class GloobusPreviewExtension(nautilus.MenuProvider):
	
	VER = '0.1'
	APP = 'nautilus-gloobus'
	MSG_BASE = '['+APP+']'
	CURRENT_FILE = ''
	CURRENT_WINDOW = None

	def can_preview(self, widget):
		#Check if i'm on an Icon (and not editing it)
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
		#TODO: implement editable hotkeys
		if event.keyval == gtk.gdk.keyval_from_name('space'):
			#Check if i'm on an Icon (and not editing it)
			if self.can_preview(widget):
				#Blocking default space Action (Open File)
				widget.emit_stop_by_name('key_press_event')
				#Call Gloobus for preview				
				if self.CURRENT_FILE != '':
					subprocess.Popen(['gloobus-preview',self.CURRENT_FILE])
	
	def __init__(self):
		MSG = _('Initializing %s extension') % self.APP
		print MSG
	
	def menu_activate_cb(self, menu, file):
		#Action for menus' item
		if file.is_gone():
			return
		#Launch gloobus-preview
		subprocess.Popen(['gloobus-preview', urllib.unquote(file.get_uri()[7:])])

	def setup_key_event(self, window):
		#Bind key_event to current window
		window.connect('key_press_event', self.on_key_press_event)
	
	#Invoked on window change , directory change
	def get_toolbar_items(self, window, file):
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
	
	#Invoked on file selection, and other file actions
	def get_file_items(self, window, files):
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
