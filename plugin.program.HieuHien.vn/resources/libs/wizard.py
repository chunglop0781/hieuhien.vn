# -*- coding: utf-8 -*-
################################################################################
#      Copyright (C) 2015 Surfacingx                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, HTMLParser, glob, json
import shutil
import errno
import string
import random
import urllib2,urllib
import re
import downloader
import extract
import time
from datetime import date, datetime, timedelta
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from string import digits

reload(sys);
sys.setdefaultencoding("utf8")

ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = '[COLOR lime]HieuHien.vn[/COLOR] - [COLOR cyan]facebook.com/HieuHien.vn[/COLOR]'
ADDON          = xbmcaddon.Addon(id='plugin.program.HieuHien.vn')
VERSION        = ADDON.getAddonInfo('version')
USER_AGENT     = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
DIALOG         = xbmcgui.Dialog()
DP             = xbmcgui.DialogProgress()
HOME           = xbmc.translatePath('special://home/')
XBMC           = xbmc.translatePath('special://xbmc/')
LOG            = xbmc.translatePath('special://logpath/')
PROFILE        = xbmc.translatePath('special://profile/')
SOURCE         = xbmc.translatePath('source://')
ADDONS         = os.path.join(HOME,      'addons')
USERDATA       = os.path.join(HOME,      'userdata')
PLUGIN         = os.path.join(ADDONS,    ADDON_ID)
PACKAGES       = os.path.join(ADDONS,    'packages')
ADDOND         = os.path.join(USERDATA,  'addon_data')
ADDONDATA      = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADVANCED       = os.path.join(USERDATA,  'advancedsettings.xml')
SOURCES        = os.path.join(USERDATA,  'sources.xml')
GUISETTINGS    = os.path.join(USERDATA,  'guisettings.xml')
FAVOURITES     = os.path.join(USERDATA,  'favourites.xml')
PROFILES       = os.path.join(USERDATA,  'profiles.xml')
THUMBS         = os.path.join(USERDATA,  'Thumbnails')
DATABASE       = os.path.join(USERDATA,  'Database')
FANART         = os.path.join(PLUGIN,    'fanart.jpg')
ICON           = os.path.join(PLUGIN,    'icon.png')
WIZLOG         = os.path.join(ADDONDATA, 'wizard.log')
SKIN           = xbmc.getSkinDir()
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
TWODAYS        = TODAY + timedelta(days=2)
THREEDAYS      = TODAY + timedelta(days=3)
ONEWEEK        = TODAY + timedelta(days=7)
KODIV          = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
if KODIV > 17:
	import zfile as zipfile #FTG mod for Kodi 18
else:
	import zipfile

BUILDFILE      = 'https://raw.githubusercontent.com/tremocoivo/repo.kongnghe.net/master/wizard.txt'
COLOR1         = 'white'
COLOR2         = 'white'
BACKUPLOCATION = ADDON.getSetting('zipdir') if not ADDON.getSetting('zipdir') == '' else 'special://home/'
MYBUILDS       = os.path.join(BACKUPLOCATION, '', '')
LOGFILES       = ['log', 'xbmc.old.log', 'kodi.log', 'kodi.old.log', 'spmc.log', 'spmc.old.log', 'tvmc.log', 'tvmc.old.log']
DEFAULTPLUGINS = ['metadata.album.universal', 'metadata.artists.universal', 'metadata.common.fanart.tv', 'metadata.common.imdb.com', 'metadata.common.musicbrainz.org', 'metadata.themoviedb.org', 'metadata.tvdb.com', 'service.xbmc.versioncheck']


###########################
###### Settings Items #####
###########################

def getS(name):
	try: return ADDON.getSetting(name)
	except: return False


def openS(name=""):
	ADDON.openSettings()



###########################
###### Display Items ######
###########################


def TextBox(title, msg):
	class TextBoxes(xbmcgui.WindowXMLDialog):
		def onInit(self):
			self.title      = 101
			self.msg        = 102
			self.scrollbar  = 103
			self.okbutton   = 201
			self.showdialog()

		def showdialog(self):
			self.getControl(self.title).setLabel(title)
			self.getControl(self.msg).setText(msg)
			self.setFocusId(self.scrollbar)
			
		def onClick(self, controlId):
			if (controlId == self.okbutton):
				self.close()
		
		def onAction(self, action):
			if   action == ACTION_PREVIOUS_MENU: self.close()
			elif action == ACTION_NAV_BACK: self.close()
			
	tb = TextBoxes( "Textbox.xml" , ADDON.getAddonInfo('path'), 'DefaultSkin', title=title, msg=msg)
	tb.doModal()
	del tb


def LogNotify(title, message, times=2000, icon=ICON,sound=False):
	DIALOG.notification(title, message, icon, int(times), sound)
	#ebi('XBMC.Notification(%s, %s, %s, %s)' % (title, message, times, icon))

def percentage(part, whole):
	return 100 * float(part)/float(whole)

###########################
###### Misc Functions #####
###########################

def getKeyboard( default="", heading="", hidden=False ):
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if keyboard.isConfirmed():
		return unicode( keyboard.getText(), "utf-8" )
	return default

def convertSize(num, suffix='B'):
	for unit in ['', 'K', 'M', 'G']:
		if abs(num) < 1024.0:
			return "%3.02f %s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.02f %s%s" % (num, 'G', suffix)

def log(msg, level=xbmc.LOGDEBUG):
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if not os.path.exists(WIZLOG): f = open(WIZLOG, 'w'); f.close()
	
	try:
		if isinstance(msg, unicode):
			msg = '%s' % (msg.encode('utf-8'))
		xbmc.log('%s: %s' % (ADDONTITLE, msg), level)
	except Exception as e:
		try: xbmc.log('Logging Failure: %s' % (e), level)
		except: pass

def addonId(add):
	try: 
		return xbmcaddon.Addon(id=add)
	except:
		return False

def ebi(proc):
	xbmc.executebuiltin(proc)

def clearCrash():  
	files = []
	for file in glob.glob(os.path.join(LOG, '*crashlog*.*' and '*stacktrace*.*')):
		files.append(file)
	if len(files) > 0:
		#if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to delete the Crash logs?' % COLOR2, '[COLOR %s]%s[/COLOR] Files Found[/COLOR]' % (COLOR1, len(files)), yeslabel="[B][COLOR green]Remove Logs[/COLOR][/B]", nolabel="[B][COLOR red]Keep Logs[/COLOR][/B]"):
			for f in files:
				os.remove(f)
			#LogNotify('[COLOR %s]Clear Crash Logs[/COLOR]' % COLOR1, '[COLOR %s]%s Crash Logs Removed[/COLOR]' % (COLOR2, len(files)))
		#else: LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, ADDONTITLE), '[COLOR %s]Clear Crash Logs Cancelled[/COLOR]' % COLOR2)
	else: LogNotify('[COLOR yellow]Clear Crash Logs:[/COLOR]', '[COLOR %s]No Crash Logs Found[/COLOR]' % COLOR2)

def chunks(s, n):
	for start in range(0, len(s), n):
		yield s[start:start+n]

def asciiCheck(use=None, over=False):
	if use == None:
		source = DIALOG.browse(3, '[COLOR %s]Select the folder you want to scan[/COLOR]' % COLOR2, 'files', '', False, False, HOME)
		if over == True:
			yes = 1
		else:
			yes = DIALOG.yesno(ADDONTITLE,'[COLOR %s]Do you want to [COLOR %s]delete[/COLOR] all filenames with special characters or would you rather just [COLOR %s]scan and view[/COLOR] the results in the log?[/COLOR]' % (COLOR2, COLOR1, COLOR1), yeslabel='[B][COLOR green]Delete[/COLOR][/B]', nolabel='[B][COLOR red]Scan[/COLOR][/B]')
	else: 
		source = use
		yes = 1

	if source == "":
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]ASCII Check: Cancelled[/COLOR]" % COLOR2)
		return
	
	files_found  = os.path.join(ADDONDATA, 'asciifiles.txt')
	files_fails  = os.path.join(ADDONDATA, 'asciifails.txt')
	afiles       = open(files_found, mode='w+')
	afails       = open(files_fails, mode='w+')
	f1           = 0; f2           = 0
	items        = fileCount(source)
	msg          = ''
	prog         = []
	log("Source file: (%s)" % str(source), xbmc.LOGNOTICE)
	
	DP.create(ADDONTITLE, 'Please wait...')
	for base, dirs, files in os.walk(source):
		dirs[:] = [d for d in dirs]
		files[:] = [f for f in files]
		for file in files:
			prog.append(file) 
			prog2 = int(len(prog) / float(items) * 100)
			DP.update(prog2,"[COLOR %s]Checking for non ASCII files" % COLOR2,'[COLOR %s]%s[/COLOR]' % (COLOR1, d), 'Please Wait[/COLOR]')
			try:
				file.encode('ascii')
			except UnicodeDecodeError:
				badfile = os.path.join(base, file)
				if yes:
					try: 
						os.remove(badfile)
						for chunk in chunks(badfile, 75):
							afiles.write(chunk+'\n')
						afiles.write('\n')
						f1 += 1
						log("[ASCII Check] File Removed: %s " % badfile, xbmc.LOGERROR)
					except:
						for chunk in chunks(badfile, 75):
							afails.write(chunk+'\n')
						afails.write('\n')
						f2 += 1
						log("[ASCII Check] File Failed: %s " % badfile, xbmc.LOGERROR)
				else:
					for chunk in chunks(badfile, 75):
						afiles.write(chunk+'\n')
					afiles.write('\n')
					f1 += 1
					log("[ASCII Check] File Found: %s " % badfile, xbmc.LOGERROR)
				pass
	DP.close(); afiles.close(); afails.close()
	total = int(f1) + int(f2)
	if total > 0:
		if os.path.exists(files_found): afiles = open(files_found, mode='r'); msg = afiles.read(); afiles.close()
		if os.path.exists(files_fails): afails = open(files_fails, mode='r'); msg2 = afails.read(); afails.close()
		if yes:
			if use:
				LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]ASCII Check: %s Removed / %s Failed.[/COLOR]" % (COLOR2, f1, f2))
			else:
				TextBox(ADDONTITLE, "[COLOR yellow][B]%s Files Removed:[/B][/COLOR]\n %s\n\n[COLOR yellow][B]%s Files Failed:[B][/COLOR]\n %s" % (f1, msg, f2, msg2))
		else: 
			TextBox(ADDONTITLE, "[COLOR yellow][B]%s Files Found:[/B][/COLOR]\n %s" % (f1, msg))
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]ASCII Check: None Found.[/COLOR]" % COLOR2)

def fileCount(home, excludes=True):
	exclude_dirs  = [ADDON_ID, 'cache', 'system', 'packages', 'Thumbnails', 'peripheral_data', 'temp', 'library', 'keymaps', '.smb']
	exclude_files = ['Textures13.db', '.DS_Store', 'Thumbs.db', '.gitignore']
	item = []
	for base, dirs, files in os.walk(home):
		if excludes:
			dirs[:] = [d for d in dirs if d not in exclude_dirs]
			files[:] = [f for f in files if f not in exclude_files]
		for file in files:
			item.append(file)
	return len(item)

##########################
###BACK UP/RESTORE #######
##########################
def backUpOptions(type, name=""):
	exclude_dirs  = ['cache', 'system', 'Thumbnails', 'peripheral_data', 'temp', 'library', 'keymaps', '.smb']
	exclude_files = ['Textures13.db', '.DS_Store', 'Thumbs.db', '.gitignore']
	bad_files     = [os.path.join(DATABASE, 'cache.db'),
					 os.path.join(DATABASE, 'DEATHScache.db'), 
					 os.path.join(DATABASE, 'DEATHScache.db-shm'), 
					 os.path.join(DATABASE, 'DEATHScache.db-wal'),
					 os.path.join(DATABASE, 'DSRDcache.lite.db'),
					 os.path.join(DATABASE, 'DSRDcache.lite.db-shm'), 
					 os.path.join(DATABASE, 'DSRDcache.lite.db-wal'),
					 os.path.join(ADDOND, 'script.trakt', 'queue.db'),
					 os.path.join(HOME, 'cache', 'commoncache.db'),
					 os.path.join(ADDOND, 'script.module.dudehere.routines', 'access.log'),
					 os.path.join(ADDOND, 'script.module.dudehere.routines', 'trakt.db'),
					 os.path.join(ADDOND, 'plugin.program.HieuHien.vn', 'settings.xml'),
					 os.path.join(ADDOND, 'script.module.metahandler', 'meta_cache', 'video_cache.db')]
	
	backup   = xbmc.translatePath(BACKUPLOCATION)
	mybuilds = xbmc.translatePath(MYBUILDS)
	
	try:
		if not os.path.exists(backup): xbmcvfs.mkdirs(backup)
		if not os.path.exists(mybuilds): xbmcvfs.mkdirs(mybuilds)
	except Exception, e:
		DIALOG.ok(ADDONTITLE, "[COLOR %s]Error making Back Up directories:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, str(e)))
		return
	if type == "build":
		#if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Are you sure you wish to backup the current build?[/COLOR]" % COLOR2, nolabel="[B][COLOR red]Cancel Backup[/COLOR][/B]", yeslabel="[B][COLOR green]Backup Build[/COLOR][/B]"):
			if name == "":
				name = getKeyboard("","Đặt tên cho file %s zip" % type)
				if not name: return False
				name = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
			name = urllib.quote_plus(name); tempzipname = ''
			zipname = os.path.join(mybuilds, '%s.zip' % name)
			for_progress  = 0
			ITEM          = []
			#if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Do you want to include your addon_data folder?" % COLOR2, 'This contains [COLOR %s]ALL[/COLOR] addon settings including passwords but may also contain important information such as skin shortcuts. We recommend [COLOR %s]MANUALLY[/COLOR] removing the addon_data folders that aren\'t required.' % (COLOR1, COLOR1), '[COLOR %s]%s[/COLOR] addon_data is ignored[/COLOR]' % (COLOR1, ADDON_ID), yeslabel='[B][COLOR green]Include data[/COLOR][/B]',nolabel='[B][COLOR red]Don\'t Include[/COLOR][/B]'):
				#exclude_dirs.append('addon_data')
			#convertSpecial(HOME, True)
			asciiCheck(HOME, True)
			#clearS('zip')
			try:
				zipf = zipfile.ZipFile(xbmc.translatePath(zipname), mode='w')
			except:
				try:
					tempzipname = os.path.join(PACKAGES, '%s.zip' % name)
					zipf = zipfile.ZipFile(tempzipname, mode='w')
				except:
					log("Không thể tạo được file %s.zip" % name, xbmc.LOGERROR)
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Không thể lưu file backup vào thư mục hiện tại, bạn có muốn đổi đường dẫn khác không?[/COLOR]" % COLOR2, yeslabel="[B][COLOR green]Đổi thư mục[/COLOR][/B]", nolabel="[B][COLOR red]Hủy[/COLOR][/B]"):
						openS()
						return
					else:
						return
			DP.create("%s[COLOR %s]: Creating Zip[/COLOR]" % (ADDONTITLE,COLOR2), "[COLOR %s]Đang tạo file backup" % COLOR2, "", "Chờ chút nhé...[/COLOR]")
			for base, dirs, files in os.walk(HOME):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					ITEM.append(file)
			N_ITEM = len(ITEM)
			#fixmetas()
			for base, dirs, files in os.walk(HOME):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					try:
						for_progress += 1
						progress = percentage(for_progress, N_ITEM) 
						DP.update(int(progress), '[COLOR %s]Đang tạo file backup: [COLOR%s]%s[/COLOR] / [COLOR%s]%s[/COLOR]' % (COLOR2, COLOR1, for_progress, COLOR1, N_ITEM), '[COLOR %s]%s[/COLOR]' % (COLOR1, file), '')
						fn = os.path.join(base, file)
						if file in LOGFILES: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join(base, file) in bad_files: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join('addons', 'packages') in fn: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.csv'): log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.pyo'): continue
						elif file.endswith('.db') and 'Database' in base:
							temp = file.replace('.db', '')
							temp = ''.join([i for i in temp if not i.isdigit()])
							#if temp in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
							if temp in ['Textures']:
								if not file == latestDB(temp):  log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						try:
							zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
						except Exception, e:
							log("[Back Up] Type = '%s': Unable to backup %s" % (type, file), xbmc.LOGNOTICE)
							log("%s / %s" % (Exception, e))
					except Exception, e:
						log("[Back Up] Type = '%s': Unable to backup %s" % (type, file), xbmc.LOGNOTICE)
						log("Build Backup Error: %s" % str(e), xbmc.LOGNOTICE)
			zipf.close()
			xbmc.sleep(500)
			#DP.update(100, "Creating %s_guisettings.zip" % name, "", "")
			#backUpOptions('guifix', name)
			if not tempzipname == '':
				success = xbmcvfs.rename(tempzipname, zipname)
				if success == 0:
					xbmcvfs.copy(tempzipname, zipname)
					xbmcvfs.delete(tempzipname)
			DP.close()
			DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR] [COLOR %s]backup thành công:[/COLOR]" % (COLOR1, name, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, zipname))
	elif type == "guifix":
		if name == "":
			guiname = getKeyboard("","Đặt tên cho file %s zip" % type)
			if not guiname: return False
			#convertSpecial(USERDATA, True)
			asciiCheck(USERDATA, True)
		else: guiname = name
		guiname = urllib.quote_plus(guiname); tempguizipname = ''
		guizipname = xbmc.translatePath(os.path.join(mybuilds, '%s_guisettings.zip' % guiname))
		if os.path.exists(GUISETTINGS):
			try:
				zipf = zipfile.ZipFile(guizipname, mode='w')
			except:
				try:
					tempguizipname = os.path.join(PACKAGES, '%s_guisettings.zip' % guiname)
					zipf = zipfile.ZipFile(tempguizipname, mode='w')
				except:
					log("Unable to create %s_guisettings.zip" % guiname, xbmc.LOGERROR)
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Không thể lưu file backup vào thư mục hiện tại, bạn có muốn đổi đường dẫn khác không?[/COLOR]" % COLOR2, yeslabel="[B][COLOR green]Đổi thư mục[/COLOR][/B]", nolabel="[B][COLOR red]Hủy[/COLOR][/B]"):
						openS()
						return
					else:
						return
			try:
				zipf.write(GUISETTINGS, 'guisettings.xml', zipfile.ZIP_DEFLATED)
				#zipf.write(PROFILES,    'profiles.xml',    zipfile.ZIP_DEFLATED)
				match = glob.glob(os.path.join(ADDOND,'skin.*', ''))
				log(str(match), xbmc.LOGNOTICE)
				for fold in match:
					fd = os.path.split(fold[:-1])[1]
					if not fd in ['skin.confluence', 'skin.re-touch', 'skin.estuary', 'skin.estouchy']:
						if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Bạn có muốn sao lưu thư mục giao diện này vào file GuiFix Zip?[/COLOR]" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, fd), yeslabel="[B][COLOR green]Add Skin[/COLOR][/B]", nolabel="[B][COLOR red]Skip Skin[/COLOR][/B]"):
							for base, dirs, files in os.walk(os.path.join(ADDOND,fold)):
								files[:] = [f for f in files if f not in exclude_files]
								for file in files:
									fn = os.path.join(base, file)
									zipf.write(fn, fn[len(USERDATA):], zipfile.ZIP_DEFLATED)
							match  = parseDOM(link, 'import', ret='addon')
							if 'script.skinshortcuts' in match:
								for base, dirs, files in os.walk(os.path.join(ADDOND,'script.skinshortcuts')):
									files[:] = [f for f in files if f not in exclude_files]
									for file in files:
										fn = os.path.join(base, file)
										zipf.write(fn, fn[len(USERDATA):], zipfile.ZIP_DEFLATED)
						else: log("[Back Up] Type = '%s': %s ignored" % (type, fold), xbmc.LOGNOTICE)
			except Exception, e:
				log("[Back Up] Type = '%s': %s" % (type, e), xbmc.LOGNOTICE)
				pass
			zipf.close()
			if not tempguizipname == '':
				success = xbmcvfs.rename(tempguizipname, guizipname)
				if success == 0:
					xbmcvfs.copy(tempguizipname, guizipname)
					xbmcvfs.delete(tempguizipname)
		else: log("[Back Up] Type = '%s': guisettings.xml not found" % type, xbmc.LOGNOTICE)
		if name == "":
			DIALOG.ok(ADDONTITLE, "[COLOR %s]GuiFix sao lưu thành công:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, guizipname))
	
	elif type == "addondata":
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Bạn có muốn sao lưu thư mục Addon_data?[/COLOR]" % COLOR2, nolabel="[B][COLOR red]Hủy[/COLOR][/B]", yeslabel="[B][COLOR green]Sao lưu ngay[/COLOR][/B]"):
			if name == "":
				name = getKeyboard("","Đặt tên cho file %s zip" % type)
				if not name: return False
				name = urllib.quote_plus(name)
			name = '%s_addondata.zip' % name; tempzipname = ''
			zipname = os.path.join(mybuilds, name)
			try:
				zipf = zipfile.ZipFile(xbmc.translatePath(zipname), mode='w')
			except:
				try:
					tempzipname = os.path.join(PACKAGES, '%s.zip' % name)
					zipf = zipfile.ZipFile(tempzipname, mode='w')
				except:
					log("Unable to create %s_addondata.zip" % name, xbmc.LOGERROR)
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Không thể lưu file backup vào thư mục hiện tại, bạn có muốn đổi đường dẫn khác không?[/COLOR]" % COLOR2, yeslabel="[B][COLOR green]Đổi thư mục[/COLOR][/B]", nolabel="[B][COLOR red]Hủy[/COLOR][/B]"):
						openS()
						return
					else:
						return
			for_progress  = 0
			ITEM          = []
			#convertSpecial(ADDOND, True)
			asciiCheck(ADDOND, True)
			DP.create("[COLOR %s]%s[/COLOR][COLOR %s]: Creating Zip[/COLOR]" % (COLOR1, ADDONTITLE,COLOR2), "[COLOR %s]Đang tạo file zip" % COLOR2, "", "Chờ chút nhé...[/COLOR]")
			for base, dirs, files in os.walk(ADDOND):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					ITEM.append(file)
			N_ITEM = len(ITEM)
			for base, dirs, files in os.walk(ADDOND):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					try:
						for_progress += 1
						progress = percentage(for_progress, N_ITEM) 
						DP.update(int(progress), '[COLOR %s]Đang tạo file zip: [COLOR%s]%s[/COLOR] / [COLOR%s]%s[/COLOR]' % (COLOR2, COLOR1, for_progress, COLOR1, N_ITEM), '[COLOR %s]%s[/COLOR]' % (COLOR1, file), '')
						fn = os.path.join(base, file)
						if file in LOGFILES: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join(base, file) in bad_files: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join('addons', 'packages') in fn: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.csv'): log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.db') and 'Database' in base:
							temp = file.replace('.db', '')
							temp = ''.join([i for i in temp if not i.isdigit()])
							if temp in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
								if not file == latestDB(temp):  log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						try:
							zipf.write(fn, fn[len(ADDOND):], zipfile.ZIP_DEFLATED)
						except Exception, e:
							log("[Back Up] Type = '%s': Unable to backup %s" % (type, file), xbmc.LOGNOTICE)
							log("Backup Error: %s" % str(e), xbmc.LOGNOTICE)
					except Exception, e:
						log("[Back Up] Type = '%s': Unable to backup %s" % (type, file), xbmc.LOGNOTICE)
						log("Backup Error: %s" % str(e), xbmc.LOGNOTICE)
			zipf.close()
			if not tempzipname == '':
				success = xbmcvfs.rename(tempzipname, zipname)
				if success == 0:
					xbmcvfs.copy(tempzipname, zipname)
					xbmcvfs.delete(tempzipname)
			DP.close()
			DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR] [COLOR %s]sao lưu thành công:[/COLOR]" % (COLOR1, name, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, zipname))

def restoreLocal(type):
	backup   = xbmc.translatePath(BACKUPLOCATION)
	mybuilds = xbmc.translatePath(MYBUILDS)
	try:
		if not os.path.exists(backup): xbmcvfs.mkdirs(backup)
		if not os.path.exists(mybuilds): xbmcvfs.mkdirs(mybuilds)
	except Exception, e:
		DIALOG.ok(ADDONTITLE, "[COLOR %s]Error making Back Up directories:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, str(e)))
		return
	file = DIALOG.browse(1, '[COLOR %s]Chọn file muốn Khôi phục[/COLOR]' % COLOR2, 'files', '.zip', False, False, mybuilds)
	#log("[RESTORE BACKUP %s] File: %s " % (type.upper(), file), xbmc.LOGNOTICE)
	if file == "" or not file.endswith('.zip'):
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR yellow]Khôi phục Kodi:[/COLOR] Đã bị hủy")
		return
	DP.create(ADDONTITLE,'[COLOR %s]Đang giải nén file' % COLOR2,'', 'Chờ chút nhé[/COLOR]')
	if not os.path.exists(USERDATA): os.makedirs(USERDATA)
	if not os.path.exists(ADDOND): os.makedirs(ADDOND)
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	if type == "gui": loc = USERDATA
	elif type == "addondata": 
		loc = ADDOND
	else : loc = HOME
	log("Restoring to %s" % loc, xbmc.LOGNOTICE)
	display = os.path.split(file)
	fn = display[1]
	try:
		zipfile.ZipFile(file,  'r')
	except:
		DP.update(0, '[COLOR %s]Không đọc được file Zip.' % COLOR2, 'Đang copy vào thư mục Packages')
		pack = os.path.join('special://home', 'addons', 'packages', fn)
		xbmcvfs.copy(file, pack)
		file = xbmc.translatePath(pack)
		DP.update(0, '', 'Copy file vào Packages: Hoàn thành')
		zipfile.ZipFile(file, 'r')
	percent, errors, error = extract.all(file,loc,DP)
	#fixmetas()
	#clearS('build')
	DP.close()
	#defaultSkin()
	#lookandFeelData('save')
	if not file.find('packages') == -1:
		try: os.remove(file)
		except: pass
	if int(errors) >= 1:
		yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, fn), 'Đã xong: [COLOR %s]%s%s[/COLOR] [Lỗi:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Bạn có muốn xem chi tiết lỗi?[/COLOR]', nolabel='[B][COLOR red]Không cần[/COLOR][/B]',yeslabel='[B][COLOR green]Xem ngay[/COLOR][/B]')
		if yes:
			if isinstance(errors, unicode):
				error = error.encode('utf-8')
			TextBox(ADDONTITLE, error.replace('\t',''))
	#setS('installed', 'true')
	#setS('extract', str(percent))
	#setS('errors', str(errors))
	#if INSTALLMETHOD == 1: todo = 1
	#elif INSTALLMETHOD == 2: todo = 0
	else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR red][B]KHÔNG DÙNG[/B][/COLOR] chức năng [B]Quit/Exit[/B] trong Kodi. Nếu cửa sổ KODI không tắt hãy khởi động lại thiết bị", nolabel='No, Cancel', yeslabel='Yes, Close')
	if todo == 0: pass
	else: killxbmc(True)

##########################
###DETERMINE PLATFORM#####
##########################

def platform():
	if xbmc.getCondVisibility('system.platform.android'):             return 'android'
	elif xbmc.getCondVisibility('system.platform.linux'):             return 'linux'
	elif xbmc.getCondVisibility('system.platform.linux.Raspberrypi'): return 'linux'
	elif xbmc.getCondVisibility('system.platform.windows'):           return 'windows'
	elif xbmc.getCondVisibility('system.platform.osx'):               return 'osx'
	elif xbmc.getCondVisibility('system.platform.atv2'):              return 'atv2'
	elif xbmc.getCondVisibility('system.platform.ios'):               return 'ios'
	elif xbmc.getCondVisibility('system.platform.darwin'):            return 'ios'


#############################
####KILL XBMC ###############
#####THANKS BRACKETS ########

def killxbmc(over=None):
	if over: choice = 1
	else: choice = DIALOG.yesno('Force Close Kodi', '[COLOR %s]You are about to close Kodi' % COLOR2, 'Would you like to continue?[/COLOR]', nolabel='[B][COLOR red] No Cancel[/COLOR][/B]',yeslabel='[B][COLOR green]Force Close Kodi[/COLOR][/B]')
	if choice == 1:
		log("Force Closing Kodi: Platform[%s]" % str(platform()), xbmc.LOGNOTICE)
		os._exit(1)