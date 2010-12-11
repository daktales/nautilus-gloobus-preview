#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# This file is part of Nautilus Gloobus Preview Extension

# Copyright (c) 2010 - 2011 - Walter Da Col <walter.dacol@gmail.com>

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

# A big thanks to Sonata team, I learned a lot from your code

from distutils.core import setup
import os
import glob
import subprocess
import sys

from sys import version
if version < '2.2.3':
	from distutils.dist import DistributionMetadata
	DistributionMetadata.classifiers = None
	DistributionMetadata.download_url = None

def removeall(path):
	if not os.path.isdir(path):
		return

	files=os.listdir(path)

	for x in files:
		fullpath=os.path.join(path, x)
		if os.path.isfile(fullpath):
			f=os.remove
			rmgeneric(fullpath, f)
		elif os.path.isdir(fullpath):
			removeall(fullpath)
			f=os.rmdir
			rmgeneric(fullpath, f)

def rmgeneric(path, __func__):
	try:
		__func__(path)
	except OSError, (errno, strerror):
		pass
			
def runcmd (cmd):
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	return out

def create_mo():
	# Create mo files:
	try:
		if not os.path.exists("mo/"):
			os.mkdir("mo/")
		for lang in ('it','es'):
			pofile = "i18n/" + lang + ".po"
			mofile = "mo/" + lang + "/nautilus-gloobus-preview.mo"
			if not os.path.exists("mo/" + lang + "/"):
				os.mkdir("mo/" + lang + "/")
			print "generating", mofile
			os.system("msgfmt %s -o %s" % (pofile, mofile))
	except Exception:
		pass
		return False
	return True

def check_pkg_config(mystdout):
	mystdout.write("Checking PKG-CONFIG...")
	if not os.path.exists(os.path.join(sys.prefix,'bin','pkg-config')):
		mystdout.write('[FAIL]\n')
		mystdout.write('\tPKG-CONFIG not found, install it first to proceed\n')
		sys.exit(1)
	mystdout.write('[OK]\n')

def get_python_nautilus_path(mystdout):
	mystdout.write('Checking PYTHON-NAUTILUS...')
	tmp = runcmd(['pkg-config','--variable=pythondir','nautilus-python']).replace('\n','')
	if  tmp != '':
		mystdout.write('[OK]\n')
		return tmp
	tmp = runcmd(['pkg-config','--variable=pythondir','python-nautilus']).replace('\n','')
	if  tmp != '':
		mystdout.write('[OK]\n')
		return tmp
	mystdout.write('[FAIL]\n')
	mystdout.write('\tPYTHON-NAUTILUS not found, install it first to proceed\n')
	sys.exit(1)

# Begin

check_pkg_config(sys.stdout)
NLIB_PATH = get_python_nautilus_path(sys.stdout).replace(sys.prefix+'/','')

# i18n
if not create_mo(): print 'Error in i18n'


setup(name = 'nautilus-gloobus-preview',
        version = '0.1.0',
        description = 'Little Nautilus extension created using nautilus-python, that bind hotkey to gloobus-preview',
        author = 'Walter Da Col',
        author_email = 'walter.dacol@gmail.com',
        url = 'https://github.com/DaKTaLeS/nautilus-gloobus-preview',
        license = 'GNU Library or Lesser General Public License (LGPL)',
        classifiers = [
              'Environment :: Plugins',
              'Environment :: X11 Applications :: GTK',
              'Environment :: X11 Applications :: Gnome',
              'Intended Audience :: End Users/Desktop',
              'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
              'Operating System :: Linux',
              'Programming Language :: Python',
           ],
        packages = ['gp_hotkey'],
        package_dir = {'gp_hotkey': 'gp_hotkey/'},
        data_files = [('share/nautilus-gloobus-preview/gp_hotkey/pixmaps',glob.glob('gp_hotkey/pixmaps/*')),
				('share/locale/it/LC_MESSAGES', ['mo/it/nautilus-gloobus-preview.mo']),
				('share/locale/es/LC_MESSAGES', ['mo/es/nautilus-gloobus-preview.mo']),
				(NLIB_PATH,['nautilus-gloobus-preview.py']),
				('bin',['gp-hotkey']),
				('share/applications',['gp-hotkey.desktop'])],
        )

# Cleanup (remove /build, /mo, and *.pyc files:
print "Cleaning up..."

try:
	removeall("build/")
	os.rmdir("build/")
except:
	pass
try:
	removeall("mo/")
	os.rmdir("mo/")
except:
	pass
try:
	for f in os.listdir("."):
		if os.path.isfile(f):
			if os.path.splitext(os.path.basename(f))[1] == ".pyc":
				os.remove(f)
except:
	pass
	
