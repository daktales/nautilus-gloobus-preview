#!/usr/bin/python
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

import pygtk
import gtk
import os
import sys
# Library for keymap mask
from libkeymask import *

class PyApp(gtk.Window):
	
	VERSION = '0.1.0'
	APPNAME = 'Nautilus Gloobus-Preview'
	PIX_DIR = ''
	USER_FILE = ''
	LAST = ['','']
	
	LAST_MOD_LIST = []
	LAST_KEY = None
	ICONTHEME = None
	HOT_ENTRY = None	
	
	# Save accelerator to file, returns status
	def save_accel_to_file(self):
		# Verify if a key is stored (accelerator can be formed by only one key)
		if (self.LAST_KEY == None):
			return '<'+_('No Hotkey pressed')+'>'
		# Check user file, if doesn't exits will create it (dir included)
		if not os.path.exists(os.path.expanduser('~/.config/nautilus-gloobus-preview')):
			os.mkdir(os.path.expanduser('~/.config/nautilus-gloobus-preview'),0755)
		# Get string from LAST_MOD_LIST and LAST_KEY
		tmp_accel_string = get_string_from_mod_list(self.LAST_MOD_LIST) + self.LAST_KEY
		# Validate string before writing to file
		if not(is_accel_string_valid(tmp_accel_string)):
			return '<'+_('No valid Hotkey pressed')+'>'
		# Writing string to file
		try:
			f = open(self.USER_FILE,'w')
			f.write(tmp_accel_string)
			f.close()
			# Set class variables
			self.LAST_MOD_LIST = []
			self.LAST_KEY = None
			return '<'+_('Done, restart Nautilus to use new binding')+'>'
		except Exception:
			return '<'+_('Save failed')+'>'
	
	# Load accelerator from user file
	def load_accel_from_file(self):
		# Check if file exists else back to default
		if not os.path.exists(self.USER_FILE):
			self.LAST_MOD_LIST = []
			self.LAST_KEY = 'space'
			return '<'+_('Default:')+' \'space\'>'
		# Reading file
		try:
			f = open(self.USER_FILE,'r')
			accel_string = f.read()
			f.close()
			if not is_accel_string_valid(accel_string):
				return '<'+_('Error in user\'s file')+'>'
			self.LAST_MOD_LIST = get_mod_list_from_accel_string(accel_string)
			self.LAST_KEY = get_key_from_accel_string(accel_string)
			return accel_string
		except Exception:
			print _('Impossible to open %s') % self.USER_FILE
			return '<Error>'
	
	def on_key_press_event(self,widget, event):
		# Fill LAST_MOD_LIST from event.state
		self.LAST_MOD_LIST = get_mod_list_from_event(event)
		# Stop key_press event
		self.emit_stop_by_name("key_press_event")
		# Set text in entry
		self.HOT_ENTRY.set_text(get_string_from_mod_list(self.LAST_MOD_LIST)+gtk.gdk.keyval_name(event.keyval))
		# Set last key pressed
		self.LAST_KEY = gtk.gdk.keyval_name(event.keyval)
	
		
	def save_accel(self, widget):
		# Saving
		tmp_string = self.save_accel_to_file()
		# Set entry text
		self.HOT_ENTRY.set_text(tmp_string)
		
	
	def load_accel(self):
		# Loading
		tmp_string = self.load_accel_from_file()
		# Set entry text
		self.HOT_ENTRY.set_text(tmp_string)
	
	def __init__(self):
		super(PyApp, self).__init__()
		
		#Set up paths
		self.USER_FILE = os.path.expanduser('~/.config/nautilus-gloobus-preview/hotkey.cfg')
		self.PIX_DIR = os.path.join(sys.prefix,'share','nautilus-gloobus-preview','gp_hotkey','pixmaps')+'/'

		#Icon and Image pixbuf
		self.ICON_THEME = gtk.icon_theme_get_default()
		win_ico = self.ICON_THEME.load_icon('gloobus-preview',64,gtk.ICON_LOOKUP_USE_BUILTIN)
		close_image = gtk.image_new_from_pixbuf(self.ICON_THEME.load_icon('window-close',32,gtk.ICON_LOOKUP_USE_BUILTIN))
		save_image = gtk.image_new_from_pixbuf(self.ICON_THEME.load_icon('document-save',32,gtk.ICON_LOOKUP_USE_BUILTIN))
		
		#Window
		self.set_size_request(360, 145)
		self.set_resizable(False)
		self.set_position(gtk.WIN_POS_CENTER)
		self.connect("destroy", gtk.main_quit)
		gtk.window_set_default_icon(win_ico)
		self.set_border_width(10)
		self.connect('key_press_event', self.on_key_press_event)
		self.set_title(self.APPNAME+' '+self.VERSION)
		
		#Entry		
		self.HOT_ENTRY = gtk.Entry()
		self.HOT_ENTRY.set_size_request(100, 30)
		
		#Try to get saved cfg
		self.load_accel()
		
		#Save Button
		save = gtk.Button(' '+_('Save'))
		save.set_size_request(100, 30)
		save.connect('clicked', self.save_accel)
		save.set_image(save_image)
		
		#Close Button
		close = gtk.Button(' '+_('Close'))
		close.set_size_request(100, 30)
		close.set_image(close_image)
		close.connect('clicked', gtk.main_quit)
		
		#Labels
		label = gtk.Label(_('Press desired hotkey then click Save button'))
		label.set_line_wrap(True)
		label.set_width_chars(25)
		label_align = gtk.Alignment(0, 0.2, 0, 0)
		label_align.add(label)
				
		#Image
		image = gtk.Image()
		image.set_from_file(self.PIX_DIR+'gloobus64.png')
		image.set_size_request(64,64)
		
		#Vbox for labels
		vbox_gp = gtk.VBox(True)
		vbox_gp.pack_start(label_align)
		
		#HBox for image
		hbox_gp = gtk.HBox(False)
		hbox_gp.pack_start(image)
		hbox_gp.pack_start(vbox_gp)
		hbox_gp.set_size_request(250, 60)
		
		#Entry label
		entry_label = gtk.Label(_('Hotkey :'))
		entry_align = gtk.Alignment(0, 1, 0, 0)
		entry_align.add(entry_label)
		entry_align.set_size_request(100, 20)
		
		#Vertical Box for buttons
		vbox_dx = gtk.VBox(False, 2)
		vbox_dx.pack_end(close,False,False,1)
		vbox_dx.pack_end(save,False,False,1)
		
		#Horizontal Box (icon,labels and buttons)
		hbox = gtk.HBox(False)
		hbox.add(hbox_gp)
		hbox.add(vbox_dx)
	
		#Main Vertical Box
		vbox_main = gtk.VBox(False, 2)
		vbox_main.set_size_request(200, 120)
		vbox_main.pack_end(gtk.Alignment(0, 0, 0, 0))
		vbox_main.pack_start(hbox,False,False,1)
		vbox_main.pack_end(self.HOT_ENTRY,False,False,1)
		vbox_main.pack_end(entry_align,False,False,1)
		
		#Last rites
		self.add(vbox_main)
		self.show_all()
		
PyApp()
gtk.main()
