# -*- coding: utf-8 -*-
####################################################################################
#                          THANK!                                                  #
# Addon nay duoc tong hop tu internet                                              #
# Tham khao code tu Addon raw.maintenance cua tac gia: Foreverska|Gombeek|Raw Media#
# Tham khao code cua Addon Areswizard                                              #
####################################################################################

import time
import ntpath
################### New Update #####################
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from datetime import date, datetime, timedelta
from urlparse import urljoin

from resources.libs import extract, downloader, wizard as wiz
#####################################################
reload(sys);
sys.setdefaultencoding("utf8")

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
base       ='https://HieuHien.vn'
ADDON      =xbmcaddon.Addon(id='plugin.program.HieuHien.vn')
dialog     = xbmcgui.Dialog()    
VERSION    = ADDON.getAddonInfo('version')
PATH       = "Trung Tam Giai Tri"            

thumbnailPath = xbmc.translatePath('special://thumbnails');
cachePath     = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath      = xbmc.translatePath('special://temp')
ADDONPATH     = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.program.HieuHien.vn')
mediaPath     = os.path.join(ADDONPATH, 'media')
databasePath  = xbmc.translatePath('special://database')
zip           =  ADDON.getSetting('zipdir')
DP            =  xbmcgui.DialogProgress()
USERDATA      =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA    =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS        =  xbmc.translatePath(os.path.join('special://home','addons'))
GUI           =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
FAVS          =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE        =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED      =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
RSS           =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS       =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
USB           =  xbmc.translatePath(os.path.join(zip))
skin          =  xbmc.getSkinDir()

################## New Update ####################################
ADDON_ID         = wiz.ADDON_ID
ADDONTITLE       = wiz.ADDONTITLE
HOME             = wiz.HOME
PACKAGES         = os.path.join(ADDONS,    'packages')
ADDOND           = os.path.join(USERDATA,  'addon_data')
ADDONDATA        = os.path.join(USERDATA,  'addon_data', ADDON_ID)
FANART           = os.path.join(ADDONPATH, 'fanart.jpg')
BACKUPLOCATION    = wiz.BACKUPLOCATION
MYBUILDS          = wiz.MYBUILDS
KODIV            = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
if KODIV > 17:
	from resources.libs import zfile as zipfile #FTG mod for Kodi 18
else:
	import zipfile
COLOR1           = wiz.COLOR1
COLOR2           = wiz.COLOR2

#######################################################################

#######################################################################
#                          CLASSES
#######################################################################

class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi
	
def MAIN():
    #setView('files', 'MAIN')
    #global analytics
    #analytics.sendPageView("HieuHien.vn","MAIN","main")
    #xbmc.executebuiltin("Container.SetViewMode(50)")
    #addItem('[COLOR red][B]HieuHien.vn[/B][/COLOR] [COLOR yellow][B]MOVIES PLAYLIST[/B][/COLOR]','url', 12,os.path.join(mediaPath, "movieslibrary.png"))
    #addDir1('[COLOR red][B]INSTALL KODI:[/B][/COLOR] Cài Đặt Kodi Full Addon','url', 14,os.path.join(mediaPath, "hieuit.wizard.png"))
    addDir1('Cài Đặt Kodi Full Addon','url', 14,os.path.join(mediaPath, "data.jpg"),FANART, '1-Click Cài Đặt Kodi Với Các Addon Thông Dụng')
    addDir1('Sao Lưu/Khôi Phục','url', 15,os.path.join(mediaPath, "backuprestore.jpg"),FANART,'Tạo Bản Kodi Để Khôi Phục Khi Cần')		
    addDir1('Cập nhật','url', 10,os.path.join(mediaPath, "update.jpg"),FANART,'Bản cập nhật sửa lỗi các addon khi dùng bản Build của HieuHien.vn')
	#addDir1('[COLOR green][B]Restore Data[/B][/COLOR] - Cho Máy Không Dùng Source [COLOR red][B]HieuHien.vn[/B][/COLOR] [COLOR yellow][B]Wizard[/B][/COLOR] ','url', 10,os.path.join(mediaPath, "restoredata.png"),FANART,'Chỉ khôi phục lại data addon mà không phải Restore bản Kodi của HieuHien.vnWizard')	
    addDir1('AdvancedSetting.xml','url', 3,os.path.join(mediaPath, "buffer.jpg"),FANART,'Tăng memcache khi xem phim không bị giật lag')
    addDir1('Công Cụ Tiện Ích','url', 4,os.path.join(mediaPath, "clean.jpg"),FANART,'Các công cụ cần thiết trong quá trình sử dụng Kodi')
    addDir1('About','url', 9,os.path.join(mediaPath, "about.jpg"),FANART,'Lets share to be shared')

def INSTALLKODI():
    setView('files', 'MAIN')
    # analytics.sendPageView("HieuHien.vn","Installkodi","HieuHien.vn")
    link = OPEN_URL('https://dl.dropboxusercontent.com/s/3sri9c3v512dk8i/Giaodien.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,1,iconimage,fanart,description)

#def restoredata():
    #analytics.sendPageView("HieuHien.vn","restoredata","Data Addon")
    #setView('videos', 'MAIN')
    #addItem('Data Addon Gdrive 0.8.66 - Dành cho Kodi 16/SPMC', 'url', 122,os.path.join(mediaPath, "gdrive.png"))
    #addItem('Data  Addon Google Drive', 'url', 13,os.path.join(mediaPath, "ggdrive.png"))
    


def restoredata():
	#link = OPEN_URL('https://dl.dropboxusercontent.com/s/x2waef04tt5aw9b/Capnhat.txt').replace('\n','').replace('\r','')
    link = OPEN_URL('https://dl.dropboxusercontent.com/s/x2waef04tt5aw9b/Capnhat.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,2,iconimage,fanart,description)
    xbmc.executebuiltin("Container.SetViewMode(500)")	

	
def BACKUP_RESTORE():
  setView('files', 'MAIN')
  #analytics.sendPageView("HieuHien.vn","backup_restore","backup_restore")
  if zip=='':
   if dialog.ok(ADDONTITLE,'Bạn chưa thiết lập đường dẫn lưu file Backup cho Kodi','Mở Addon Setting và Chọn tab [COLOR green][B]Zip Folder[/B][/COLOR].','Nhấn [B]OK[/B] để bắt đầu thiết lập'):
    ADDON.openSettings()
  else:
     #setView('files', 'MAIN')
     addDir2('[COLOR green][B]BACKUP:[/B][/COLOR] Sao lưu Kodi','url',16,os.path.join(mediaPath,"backups.jpg"),'Tạo bản Build Kodi cá nhân hóa')
     addDir2('[COLOR yellow][B]RESTORE:[/B][/COLOR] Khôi phục Kodi','url',17,os.path.join(mediaPath,"restore.jpg"),'Khôi phục lại bản build đã tạo trước đó hoặc tải trên interter')

def BACKUP_OPTION():
    #analytics.sendPageView("HieuHien.vn","backup_option","backupmenu")
    setView('files', 'MAIN')
    if not zip == '':
        addItem('Thư Mục Backup Mặc Định: [COLOR yellow]%s[/COLOR] <-- Nhấn để đổi thư mục' % (MYBUILDS),'url', 999, os.path.join(mediaPath,"dir.png"))	
        addDir2('[COLOR green][B]FULL BACKUP:[/B][/COLOR] Sao Lưu Toàn Bộ Hệ Thống','url',18,os.path.join(mediaPath,"fullbackup.png"),'Back Up Your Full System')
        #addDir2('[COLOR yellow]Backup Addons:[/COLOR] Sao luu tat ca Addon','addons',19,'','Back Up Your Addons')
        addDir2('[COLOR yellow]Backup UserData:[/COLOR] Sao Lưu Setting Tất Cả Addon','addon_data',19,os.path.join(mediaPath,"backupuserdata.png"),'Back Up Your Addon Userdata')  
        addDir2('[COLOR yellow]Backup Guisettings.xml:[/COLOR] Sao Lưu Setting Của Kodi',GUI,191,os.path.join(mediaPath,"backupsetting.png"),'Back Up Your guisettings.xml')
        if os.path.exists(FAVS):
            addDir2('[COLOR yellow]Backup Favourites:[/COLOR] Sao Lưu Mục Yêu Thích',FAVS,20,os.path.join(mediaPath,"backupFavourites.png"),'Back Up Your favourites.xml')
        if os.path.exists(SOURCE):
            addDir2('[COLOR yellow]Backup Source:[/COLOR] Sao Lưu Các Link Trong File Manager',SOURCE,20,os.path.join(mediaPath,"backupsource.png"),'Back Up Your sources.xml')
        if os.path.exists(ADVANCED):
            addDir2('[COLOR yellow]Backup AdvancedSettings:[/COLOR] Sao Lưu File Advancedsettings.xml',ADVANCED,20,os.path.join(mediaPath,"backupcachesetting.png"),'Back Up Your advancedsettings.xml')
        if os.path.exists(KEYMAPS):
            addDir2('[COLOR yellow]Backup keyboard:[/COLOR] Sao Lưu Phím Tắt Kodi',KEYMAPS,20,os.path.join(mediaPath,"backupkeymap.png"),'Back Up Your keyboard.xml')

def RESTORE_OPTION():
    setView('files', 'MAIN')
    #analytics.sendPageView("HieuHien.vn","restore_option","restoremenu")
    #if os.path.exists(os.path.join(USB,'backup.zip')):	
    addDir2('[COLOR green][B]FULL RESTORE:[/B][/COLOR] Khôi Phục Toàn Bộ Từ File Đã Backup','url',21,os.path.join(mediaPath,"fullrestore.png"),'Restore all from backup file')
        
    if os.path.exists(os.path.join(USB,'addon_data.zip')):   
        addDir2('[COLOR yellow]Restore UserData:[/COLOR] Khôi Phục Setting Các Addon','addon_data',19,os.path.join(mediaPath,"restoreuserdata.png"),'Restore Your AddonData')

    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        addDir2('[COLOR yellow]Restore Guisettings:[/COLOR] Khôi Phục Setting Của Kodi',GUI,20,os.path.join(mediaPath,"restoresetting.png"),'Restore Your guisettings.xml')
    
    if os.path.exists(os.path.join(USB,'favourites.xml')):
        addDir2('[COLOR yellow]Restore Favourites:[/COLOR] Khôi Phục Mục Yêu Thích',FAVS,20,os.path.join(mediaPath,"restorefavourite.png"),'Restore Your favourites.xml')
        
    if os.path.exists(os.path.join(USB,'sources.xml')):
        addDir2('[COLOR yellow]Restore Source:[/COLOR] Khôi Phục Link Trong File Manager',SOURCE,20,os.path.join(mediaPath,"restoresource.png"),'Restore Your sources.xml')
        
    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        addDir2('[COLOR yellow]Restore AdvancedSettings:[/COLOR] Khôi Phục File Advancedsettings.xml',ADVANCED,20,os.path.join(mediaPath,"restorecachesetting.png"),'Restore Your advancedsettings.xml')        

    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        addDir2('[COLOR yellow]Restore Keyboard:[/COLOR] Khôi Phục Phím Tắt Kodi',KEYMAPS,20,os.path.join(mediaPath,"restorekeymap.png"),'Restore Your keyboard.xml')
		
def RESTORE_ZIP_FILE(name,url):
        
    if 'addon_data' in url:
        
		wiz.backUpOptions('addondata')
    #else:
        # ZIPFILE = xbmc.translatePath(os.path.join(USB,'addon_data.zip'))
        #DIR = ADDON_DATA
		return

def RESTORE_BACKUP_XML(name,url,description):
    if 'Backup' in name:
        TO_READ   = open(url).read()
        TO_WRITE  = os.path.join(USB,description.split('Your ')[1])
        
        f = open(TO_WRITE, mode='w')
        f.write(TO_READ)
        f.close() 
         
    else:
    
        if 'guisettings.xml' in description:
            a = open(os.path.join(USB,description.split('Your ')[1])).read()
            
            r='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            
            match=re.compile(r).findall(a)
            
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&') 
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))  
        else:    
            TO_WRITE   = os.path.join(url)
            TO_READ  = open(os.path.join(USB,description.split('Your ')[1])).read()
            
            f = open(TO_WRITE, mode='w')
            f.write(TO_READ)
            f.close()  
    dialog.ok(ADDONTITLE, "", 'Đã xong!','')


def DeletePackages():
    
    xbmc.log( '############################################################       DELETING PACKAGES             ###############################################################')
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
 
    for root, dirs, files in os.walk(packages_cache_path):
        file_count = 0
        file_count += len(files)
        
    # Count files and give option to delete
        if file_count > 0:
                        
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
    for root, dirs, files in os.walk(thumbnailPath):
        file_count = 0
        file_count += len(files)
        
    # Count files and give option to delete
        if file_count > 0:
                        
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
    clearCache()
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'windows': # Windows
        return
    else:
        text13 = os.path.join(databasePath,"Textures13.db")
        os.unlink(text13)
    
	
def Tweak():
    setView('files', 'MAIN')
    #analytics.sendPageView("HieuHien.vn","Tweak","Tang Toc Cache")
    link = OPEN_URL('https://dl.dropboxusercontent.com/s/kx45j8cmbl2rfcb/buffer.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,2,iconimage,fanart,description)
    xbmc.executebuiltin("Container.SetViewMode(50)")

def UPDATE():
    setView('files', 'MAIN')
    #analytics.sendPageView("HieuHien.vn","Update","Update Addon")
    link = OPEN_URL('https://dl.dropboxusercontent.com/s/x2waef04tt5aw9b/Capnhat.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,2,iconimage,fanart,description)
    xbmc.executebuiltin("Container.SetViewMode(50)")		

    
def utilities():
    #analytics.sendPageView("HieuHien.vn","menucache","Xoa cache")
    #analytics.sendPageView("RawMaintenenance","maintenance","maint")
    setView('files', 'MAIN')
    addItem('Clear Cache - Xóa Cache','url', 5,os.path.join(mediaPath, "clearcache.jpg"))
    addItem('Delete Thumbnails - Xóa Ảnh Xem Trước Của Video/Addon', 'url', 6,os.path.join(mediaPath, "clearthumbnail.jpg"))
    addItem('Purge Packages - Xóa Các Gói Cài Đặt Cũ', 'url', 7,os.path.join(mediaPath, "clearpackage.jpg"))
    addItem('[COLOR red][B]Delete All - Xóa Tất Cả[/B][/COLOR]', 'url', 8,os.path.join(mediaPath, "deleteall.jpg"))	
    addItem('[COLOR yellow][B]Speedtest[/B][/COLOR] - Kiểm Tra Tốc Độ Mạng','url', 23,os.path.join(mediaPath, "speedtest.png"))

    
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
def wizard(name,url,description):
    ################## New code ###################################
	zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	DP.create(ADDONTITLE,'[B]Đang Tải:[/B] %s' % (name),'', 'Chờ Chút Nhé...')
	lib=os.path.join(PACKAGES, '%s.zip' % zipname)
	try: os.remove(lib)
	except: pass
	downloader.download(url, lib, DP)
	xbmc.sleep(500)
	title = '[B]Đang cài đặt:[/B] %s' % (name)
	DP.update(0, title,'', 'Chờ Chút Nhé...')
	percent, errors, error = extract.all(lib,HOME,DP, title=title)
	if int(float(percent)) > 0:
		
		wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
		try: os.remove(lib)
		except: pass
		if int(float(errors)) > 0:
			yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), 'Đã hoàn thành: [COLOR %s]%s%s[/COLOR] [Lỗi:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Bạn có muốn xem thống kê lỗi?[/COLOR]', nolabel='[B][COLOR red]Không cần[/COLOR][/B]',yeslabel='[B][COLOR green]Xem ngay[/COLOR][/B]')
			if yes:
				if isinstance(errors, unicode):
					error = error.encode('utf-8')
				wiz.TextBox(ADDONTITLE, error)
	DP.close()

def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'


def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name).decode("utf-8")+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDir1(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name).decode("utf-8")+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
	liz.setProperty( "Fanart_Image", fanart )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def addDir2(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name).decode("utf-8")+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        if mode==17 or mode==16:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
		
def addItem(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name).decode("utf-8")+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok
	
#######################################################################
#						Delete All Cache
#######################################################################
def setupCacheEntries():
    entries = 5 #make sure this refelcts the amount of entries you have
    dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
    pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
					"special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                    "special://profile/addon_data/plugin.video.itv/Images"]
                    
    cacheEntries = []
    
    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
    
    return cacheEntries


def clearCache():
    # global analytics
    # analytics.sendEvent("HieuHien.vn", "Clear Cache")
    
    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                #dialog = xbmcgui.Dialog()
                #if dialog.yesno("Delete XBMC Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            if (f == "xbmc.log" or f == "xbmc.old.log"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                #dialog = xbmcgui.Dialog()
                #if dialog.yesno("Delete XBMC Temp Files", str(file_count) + " files found", "Do you want to delete them?"):
                    for f in files:
                        try:
                            if (f == "xbmc.log" or f == "xbmc.old.log"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                #dialog = xbmcgui.Dialog()
                #if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                #dialog = xbmcgui.Dialog()
                #if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:

                    #dialog = xbmcgui.Dialog()
                    #if dialog.yesno("Raw Manager",str(file_count) + "%s cache files found"%(entry.name), "Do you want to delete them?"):
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass
                

    dialog = xbmcgui.Dialog()
    #dialog.ok("HieuHien.vn", "Done Clearing Cache files")
    
    
def deleteThumbnails():
    # global analytics
    # analytics.sendEvent("HieuHien.vn", "Delete thumb")
    
    if os.path.exists(thumbnailPath)==True:  
            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete Thumbnails", "This option deletes all thumbnails", "Are you sure you want to do this?"):
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
                                pass                
    else:
        pass
    
    text13 = os.path.join(databasePath,"Textures13.db")
    os.unlink(text13)
        
    dialog.ok("Restart XBMC", "Please restart XBMC to rebuild thumbnail library")
        
def purgePackages():
    # global analytics
    # analytics.sendEvent("HieuHien.vn", "del package")
    
    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    #if dialog.yesno("Delete Package Cache Files", "%d packages found."%file_count, "Delete Them?"):  
        #for root, dirs, files in os.walk(purgePath):
            #file_count = 0
            #file_count += len(files)
            if file_count > 0:            
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
                dialog = xbmcgui.Dialog()
                dialog.ok("HieuHien.vn", "Deleting Packages all done")
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok("HieuHien.vn", "No Packages to Purge")       
				

def restoreggdrive():
    # global analytics
    # analytics.sendEvent("HieuHien.vn", "restore ggdrive")
    y = dialog.yesno("[COLOR red][B]CẢNH BÁO !!![/COLOR][/B]", "Tất cả [COLOR yellow]Account đã thêm vào Google Drive[/COLOR] sẽ bị ghi đè.", "Bạn có muốn tiếp tục?") 
    if y == 0:   
        pass
    else:
        wizard("dataggdrive",'https://dl.dropboxusercontent.com/s/nofqcb6rd9l7v6i/data_ggdrive.zip',description)
        dialog.ok("Done!", "Khôi phục xong, nhấn OK và thưởng thức ^^")
        xbmc.executebuiltin('RunAddon(plugin.googledrive)')		

def restoregdrive():
    # global analytics
    # analytics.sendEvent("HieuHien.vn", "restore gdrive")
    y = dialog.yesno("[COLOR red][B]CẢNH BÁO !!![/COLOR][/B]", "Tất cả [COLOR yellow]Account đã thêm vào GDrive[/COLOR] sẽ bị ghi đè.", "Bạn có muốn tiếp tục?") 
    if y == 0:   
        pass
    else:
        wizard("dataggdrive",'https://dl.dropboxusercontent.com/s/82w2elvg2t2kood/data_gdrive.zip',description)
        dialog.ok("Done!", "Khôi phục xong, nhấn OK và thưởng thức ^^")
        xbmc.executebuiltin('RunAddon(plugin.video.gdrive)')

def speedMenu():
	xbmc.executebuiltin('Runscript("special://home/addons/plugin.program.HieuHien.vn/speedtest.py")')
	
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
#setupAnalytics()        
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
 
        
if mode==None or url==None or len(url)<1:
        MAIN()
       
elif mode==1:
        wizard(name,url,description)
        dialog.ok(ADDONTITLE, '[COLOR yellow]Đã cài đặt thành công![/COLOR]', 'Nhấn [B]OK[/B] để thoát Kodi')
        #killxbmc()
        wiz.killxbmc(True)
        
elif mode==2:
        wizard(name,url,description)
        dialog.ok("DONE!", 'Đã cài đặt xong. Khởi động lại Kodi để kiểm tra.')		
        
		
elif mode==3:
        Tweak()
		
elif mode==4:
        utilities()
		
elif mode==5:
        clearCache()
        dialog.ok("HieuHien.vn", "Done Clearing Cache files")		
        
elif mode==6:
        deleteThumbnails()
        
elif mode==7:
        purgePackages()
        
elif mode==8:
        clearCache()
        dialog.ok("HieuHien.vn", "Done Clearing Cache files")	
        purgePackages()
        deleteThumbnails()
        	

elif mode==9:		
    xbmcaddon.Addon(id='plugin.program.HieuHien.vn').openSettings()
    	
elif mode==10:
        restoredata()
        	

elif mode==11:
        restorelibrary()       		

elif mode==12:
        #restoregdrive()
        xbmc.executebuiltin('ActivateWindow(10025,plugin://plugin.video.thongld.vnplaylist/section/0@1l6TcaMsEINocqUPyLF0mhSBUW5y36tDwVDXpXImx4eY/%5BCOLOR+yellow%5DMovies+%28by+HieuIT%29%5B%2FCOLOR%5D,return)')

elif mode==122:
        restoregdrive()		

elif mode==13:
        restoreggdrive()
		
elif mode==14:
        INSTALLKODI()

elif mode==15:
    BACKUP_RESTORE()

elif mode==16:
        BACKUP_OPTION()

elif mode==17:
        RESTORE_OPTION()	

elif mode==18:
		wiz.backUpOptions('build')

elif mode==19:
        RESTORE_ZIP_FILE(name,url)		
		
elif mode==20:
        RESTORE_BACKUP_XML(name,url,description)
		
elif mode==21:
        #RESTORE()
        wiz.restoreLocal(type)

elif mode==191      : wiz.backUpOptions('guifix')
		
elif mode==22:
        UPDATE()

elif mode==23:
       speedMenu()
       		
		
elif mode==999:
        dialog.ok(ADDONTITLE, 'Thay đổi thư mục Backup mặc định trong tab [COLOR yellow]Zip Folder[/COLOR]', 'Nhấn [B]OK[/B] để bắt đầu')
        ADDON.openSettings()
		
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))

