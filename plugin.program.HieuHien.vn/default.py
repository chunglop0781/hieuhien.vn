####################################################################################
#                          THANK!                                                  #
# Addon nay duoc tong hop tu internet - dua tren addon HieuITWizard                #
# Tham khao code tu Addon raw.maintenance cua tac gia: Foreverska|Gombeek|Raw Media#
# Tham khao code cua Addon usbwizard cua tac gia: LittleWiz                        #
####################################################################################
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re
import extract
import time
import downloader
import plugintools
import zipfile
import ntpath
import GATracker
import uuid

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base       ='https://HieuHien.vn'
ADDON      =xbmcaddon.Addon(id='plugin.program.HieuHien.vn')
dialog     = xbmcgui.Dialog()    
VERSION    = "1.1.0"
PATH       = "Kodi HieuHien.vn"            

thumbnailPath = xbmc.translatePath('special://thumbnails');
cachePath     = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath      = xbmc.translatePath('special://temp')
addonPath     = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.program.HieuHien.vn')
mediaPath     = os.path.join(addonPath, 'media')
databasePath  = xbmc.translatePath('special://database')
zip           =  ADDON.getSetting('zip')
dp            =  xbmcgui.DialogProgress()
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




#######################################################################
#                          CLASSES
#######################################################################

class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi

#######################################################################
#						Google Analytics
#######################################################################
global analytics

def setupAnalytics():
    global analytics

    if(os.path.isfile(os.path.join(addonPath, "uuid.txt")) != True):
        userID = uuid.uuid1()
        uuidFile = open(os.path.join(addonPath,"uuid.txt"), "w")
        uuidFile.write(str(userID))
        uuidFile.close()

    uuidFile = open(os.path.join(addonPath, "uuid.txt"), "r")
    userID = uuidFile.readline()
    uuidFile.close()

    analytics = GATracker.GAconnection("UA-89364622-1", userID)
########################################################################
	
def MAIN():
    #setView('movies', 'MAIN')
    global analytics
    analytics.sendPageView("Kodi HieuHien.vn","MAIN","main")
    xbmc.executebuiltin("Container.SetViewMode(50)")	
    addDir1('Cai dat Kodi Full Addon','url', 14,os.path.join(mediaPath, "data.jpg"))
    addDir1('Backup Restore','url', 15,os.path.join(mediaPath, "backuprestore.jpg"))		
    addDir1('Cap nhat','url', 10,os.path.join(mediaPath, "update.jpg"))	
    addDir1('AdvancedSetting.xml','url', 3,os.path.join(mediaPath, "buffer.jpg"))
    addDir1('Clear cache','url', 4,os.path.join(mediaPath, "clean.jpg"))
    addDir1('About','url', 9,os.path.join(mediaPath, "about.jpg"))

def INSTALLKODI():
    analytics.sendPageView("Kodi HieuHien.vn","Installkodi","Kodi HieuHien.vn")
    link = OPEN_URL('https://dl.dropboxusercontent.com/s/3sri9c3v512dk8i/Giaodien.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,1,iconimage,fanart,description)
		
def BACKUP_RESTORE():
  analytics.sendPageView("Kodi HieuHien.vn","backup_restore","backup_restore")
  if zip=='':
   if dialog.ok('[COLOR lime][B]HieuHien.vn[/B][/COLOR]','Ban chua thiet lap duong dan luu file Backup cho Kodi','Mo Addon Setting va Chon tabb [COLOR green][B]Zip Folder[/B][/COLOR].','Nhan [B]OK[/B] de bat dau thiet lap'):
    ADDON.openSettings()
  else:
     xbmc.executebuiltin("Container.SetViewMode(50)")
     addDir1('[COLOR green][B]BACKUP:[/B][/COLOR] Sao luu Kodi','url',16,os.path.join(mediaPath,"backups.jpg"))
     addDir1('[COLOR yellow][B]RESTORE:[/B][/COLOR] Khoi phuc Kodi','url',17,os.path.join(mediaPath,"restores.jpg"))

def BACKUP_OPTION():
    analytics.sendPageView("Kodi HieuHien.vn","backup_option","backupmenu")
    xbmc.executebuiltin("Container.SetViewMode(50)")
    if not zip == '': 
        addDir2('[COLOR green][B]FULL BACKUP:[/B][/COLOR] Sao luu toan bo he thong','url',18,os.path.join(mediaPath,"fullbackup.png"),'Back Up Your Full System')
        #addDir2('[COLOR yellow]Backup Addons:[/COLOR] Sao luu tat ca Addon','addons',19,'','Back Up Your Addons')
        addDir2('[COLOR yellow]Backup UserData:[/COLOR] Sao luu Setting cac Addon','addon_data',19,os.path.join(mediaPath,"backupuserdata.png"),'Back Up Your Addon Userdata')  
        addDir2('[COLOR yellow]Backup Guisettings.xml:[/COLOR] Sao luu cac Setting cua Kodi',GUI,20,os.path.join(mediaPath,"backupsetting.png"),'Back Up Your guisettings.xml')
        if os.path.exists(FAVS):
            addDir2('[COLOR yellow]Backup Favourites:[/COLOR] Sao luu muc Yeu thich',FAVS,20,os.path.join(mediaPath,"backupFavourites.png"),'Back Up Your favourites.xml')
        if os.path.exists(SOURCE):
            addDir2('[COLOR yellow]Backup Source:[/COLOR] Sao luu cac link trong File Manager',SOURCE,20,os.path.join(mediaPath,"backupsource.png"),'Back Up Your sources.xml')
        if os.path.exists(ADVANCED):
            addDir2('[COLOR yellow]Backup AdvancedSettings:[/COLOR] Sao luu file Advancedsettings.xml',ADVANCED,20,os.path.join(mediaPath,"backupcachesetting.png"),'Back Up Your advancedsettings.xml')
        if os.path.exists(KEYMAPS):
            addDir2('[COLOR yellow]Backup keyboard:[/COLOR] Sao luu phim tat Kodi',KEYMAPS,20,os.path.join(mediaPath,"backupkeymap.png"),'Back Up Your keyboard.xml')
        

def RESTORE_OPTION():
    analytics.sendPageView("Kodi HieuHien.vn","restore_option","restoremenu")
    if os.path.exists(os.path.join(USB,'backup.zip')):   
        addDir2('[COLOR green][B]FULL RESTORE:[/B][/COLOR] Khoi phuc day du addon, skin, setting...','url',21,os.path.join(mediaPath,"fullrestore.png"),'Khoi phuc tat ca')
        
    if os.path.exists(os.path.join(USB,'addon_data.zip')):   
        addDir2('[COLOR yellow]Restore UserData:[/COLOR] Khoi phuc Setting cac Addon','addon_data',19,os.path.join(mediaPath,"restoreuserdata.png"),'Restore Your AddonData')

    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        addDir2('[COLOR yellow]Restore Guisettings:[/COLOR] Khoi phuc Setting cua Kodi',GUI,20,os.path.join(mediaPath,"restoresetting.png"),'Restore Your guisettings.xml')
    
    if os.path.exists(os.path.join(USB,'favourites.xml')):
        addDir2('[COLOR yellow]Restore Favourites:[/COLOR] Khoi phuc muc Yeu thich',FAVS,20,os.path.join(mediaPath,"restorefavourite.png"),'Restore Your favourites.xml')
        
    if os.path.exists(os.path.join(USB,'sources.xml')):
        addDir2('[COLOR yellow]Restore Source:[/COLOR] Khoi phuc link trong File Manager',SOURCE,20,os.path.join(mediaPath,"restoresource.png"),'Restore Your sources.xml')
        
    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        addDir2('[COLOR yellow]Restore AdvancedSettings:[/COLOR] Khoi phuc file Advancedsettings.xml',ADVANCED,20,os.path.join(mediaPath,"restorecachesetting.png"),'Restore Your advancedsettings.xml')        

    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        addDir2('[COLOR yellow]Restore Keyboard:[/COLOR] Khoi phuc phim tat Kodi',KEYMAPS,20,os.path.join(mediaPath,"restorekeymap.png"),'Restore Your keyboard.xml')
        

def BACKUP():  
    global analytics
    analytics.sendEvent("HieuHien.vn Kodi", "backup")
    to_backup = xbmc.translatePath(os.path.join('special://','home'))
    backup_zip = xbmc.translatePath(os.path.join(USB,'backup.zip'))
    DeletePackages()    
    #import zipfile
    
    dp.create("[COLOR lime][B]HieuHien.vn[/B][/COLOR]","Backing Up",'', 'Please Wait')
    zipobj = zipfile.ZipFile(backup_zip , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(to_backup)
    for_progress = []
    ITEM =[]
    for base, dirs, files in os.walk(to_backup):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(to_backup):
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
            fn = os.path.join(base, file)
            if not 'temp' in dirs:
                if not 'plugin.program.HieuHien.vn' in dirs:
                   #import time
                   CUNT= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   if FILE_DATE > CUNT:
                       zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()
    dialog.ok("[COLOR lime][B]HieuHien.vn[/B][/COLOR]", "Da tao xong file Backup", '','')

def READ_ZIP(url):

    #import zipfile
    
    z = zipfile.ZipFile(url, "r")
    for filename in z.namelist():
        if 'guisettings.xml' in filename:
            a = z.read(filename)
            r='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            
            match=re.compile(r).findall(a)
            
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&') 
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))  
                
        if 'favourites.xml' in filename:
            a = z.read(filename)
            f = open(FAVS, mode='w')
            f.write(a)
            f.close()  
			               
        if 'sources.xml' in filename:
            a = z.read(filename)
            f = open(SOURCE, mode='w')
            f.write(a)
            f.close()    
                         
        if 'advancedsettings.xml' in filename:
            a = z.read(filename)
            f = open(ADVANCED, mode='w')
            f.write(a)
            f.close()                 

        if 'RssFeeds.xml' in filename:
            a = z.read(filename)
            f = open(RSS, mode='w')
            f.write(a)
            f.close()                 
            
        if 'keyboard.xml' in filename:
            a = z.read(filename)
            f = open(KEYMAPS, mode='w')
            f.write(a)
            f.close()                 
              
def RESTORE():
    global analytics
    analytics.sendEvent("Kodi HieuHien.vn", "restore")
    #import time
    dialog = xbmcgui.Dialog()
        
    lib=xbmc.translatePath(os.path.join(zip,'backup.zip'))
    READ_ZIP(lib)
    dp.create("[COLOR lime][B]HieuHien.vn[/B][/COLOR]","Dang kiem tra... ",'', 'Cho chut nha!')
    HOME = xbmc.translatePath(os.path.join('special://','home'))
    
    dp.update(0,"", "[B]Dang giai nen file....[/B]")
    extract.all(lib,HOME,dp)
    time.sleep(1)
    xbmc.executebuiltin('UpdateLocalAddons ')    
    xbmc.executebuiltin("UpdateAddonRepos")
    #xbmc.executebuiltin('UnloadSkin()') 
    #xbmc.executebuiltin('ReloadSkin()')
    #dialog.ok("[COLOR red][B][COLOR lime][B]HieuHien.vn[/B][/COLOR][/B][/COLOR]", "Khoi dong lai thiet bi neu Kodi khong thay doi", "","")
    #xbmc.executebuiltin("LoadProfile(Master user)")
    killxbmc()	

def RESTORE_ZIP_FILE(name,url):
        
    if 'addons' in url:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addons.zip'))
        DIR = ADDONS
        to_backup = ADDONS
        
        backup_zip = xbmc.translatePath(os.path.join(USB,'addons.zip'))
    else:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addon_data.zip'))
        DIR = ADDON_DATA

        
    if 'Backup' in name:
        DeletePackages() 
        #import zipfile
        #import sys
        dp.create("[COLOR lime][B]HieuHien.vn[/B][/COLOR]","Dang tao file Backup",'', 'Cho chut nha!')
        zipobj = zipfile.ZipFile(ZIPFILE , 'w', zipfile.ZIP_DEFLATED)
        rootlen = len(DIR)
        for_progress = []
        ITEM =[]
        for base, dirs, files in os.walk(DIR):
            for file in files:
                ITEM.append(file)
        N_ITEM =len(ITEM)
        for base, dirs, files in os.walk(DIR):
            for file in files:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Cho chut nha!')
                fn = os.path.join(base, file)
                if not 'temp' in dirs:
                    if not 'plugin.program.HieuHien.vn' in dirs:
                       #import time
                       CUNT= '01/01/1980'
                       FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                       if FILE_DATE > CUNT:
                           zipobj.write(fn, fn[rootlen:]) 
        zipobj.close()
        dp.close()
        dialog.ok("[COLOR red][B]HieuHien.vn[/B][/COLOR]", "Da tao xong file Backup", '','')   
    else:

        dp.create("[COLOR red][B]HieuHien.vn[/B][/COLOR]","Dang kiem tra... ",'', 'Cho chut nha!')
        
        #import time
        dp.update(0,"", "[B]Dang giai nen file....[/B]")
        extract.all(ZIPFILE,DIR,dp)
        
        time.sleep(1)
        xbmc.executebuiltin('UpdateLocalAddons ')    
        xbmc.executebuiltin("UpdateAddonRepos")
        dialog.ok("[COLOR red][B]HieuHien.vn[/B][/COLOR]", "Da khoi phuc xong.", '','')
      

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
    dialog.ok("[COLOR red][B]HieuHien.vn[/B][/COLOR]", "", 'Da xong!','')


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
    

def restoredata():
	#link = OPEN_URL('https://dl.dropboxusercontent.com/s/x2waef04tt5aw9b/Capnhat.txt').replace('\n','').replace('\r','')
    link = OPEN_URL('https://dl.dropboxusercontent.com/s/x2waef04tt5aw9b/Capnhat.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,2,iconimage,fanart,description)
    xbmc.executebuiltin("Container.SetViewMode(500)")	
    
	
def Tweak():
    analytics.sendPageView("Kodi HieuHien.vn","Tweak","Tang Toc Cache")
    link = OPEN_URL('https://dl.dropboxusercontent.com/s/kx45j8cmbl2rfcb/buffer.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,2,iconimage,fanart,description)
    xbmc.executebuiltin("Container.SetViewMode(50)")	

    
def menucache():
    analytics.sendPageView("Kodi HieuHien.vn","menucache","Xoa cache")
    #analytics.sendPageView("RawMaintenenance","maintenance","maint")
    xbmc.executebuiltin("Container.SetViewMode(500)")
    addItem('Xoa Cache - Clear Cache','url', 5,os.path.join(mediaPath, "clearcache.jpg"))
    addItem('Xoa Anh Thu Nho Video - Delete Thumbnails', 'url', 6,os.path.join(mediaPath, "clearthumbnail.jpg"))
    addItem('Xoa Goi Cai Dat Cu - Purge Packages', 'url', 7,os.path.join(mediaPath, "clearpackage.jpg"))
    addItem('[COLOR red][B]Don Tat Ca - Delete All[/B][/COLOR]', 'url', 8,os.path.join(mediaPath, "deleteall.jpg"))	

    
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
def wizard(name,url,description):
    global analytics
    analytics.sendEvent("Kodi HieuHien.vn", "wizard")
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    #dp = xbmcgui.DialogProgress()
    dp.create("Kodi HieuHien.vn","[B]Dang tai file cai dat[/B]",'', "[B]Cho 1 chut nha!![/B]")
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "[B]Dang giai nen file....[/B]")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    xbmc.executebuiltin('UpdateLocalAddons')    
    xbmc.executebuiltin("UpdateAddonRepos")
    #dialog = xbmcgui.Dialog()
    #dialog.ok("DA TAI XONG", 'De cai dat vui long theo huong dan', 'De thoat Kodi ngay, Nhan OK.', 'KHONG DUNG chuc nang Quit/Exit trong Kodi., Neu cua so KODI khong tat vi ly do nao do hay Khoi dong lai thiet bi')
    #killxbmc()
        
          
def killxbmc():
    choice = xbmcgui.Dialog().yesno('[COLOR red][B]Kodi Exit!![/B][/COLOR]', '[COLOR red][B]KHONG DUNG[/B][/COLOR] chuc nang [B]Quit/Exit[/B] trong Kodi. Neu cua so KODI khong tat hay Khoi dong lai thiet bi', nolabel='No, Cancel',yeslabel='Yes, Close')
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok("[COLOR=red][B]WARNING  !!![/B][/COLOR]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Either close using Task Manager (If unsure pull the plug).")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    

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
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDir1(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def addDir2(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        if mode==17 or mode==16:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
		
def addItem(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
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
    global analytics
    analytics.sendEvent("Kodi HieuHien.vn", "Clear Cache")
    
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
    #dialog.ok("Kodi HieuHien.vn", "Done Clearing Cache files")
    
    
def deleteThumbnails():
    global analytics
    analytics.sendEvent("Kodi HieuHien.vn", "Delete thumb")
    
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
    global analytics
    analytics.sendEvent("Kodi HieuHien.vn", "del package")
    
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
                dialog.ok("Kodi HieuHien.vn", "Deleting Packages all done")
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok("Kodi HieuHien.vn", "No Packages to Purge")       

def restorelibrary():
    global analytics
    analytics.sendEvent("Kodi HieuHien.vn", "restore library")
    y = dialog.yesno("[COLOR red][B]CANH BAO !!![/COLOR][/B]", "Thu vien phim chi Play voi Data Account cai dat tu Kodi HieuHien.vn","Tat ca [COLOR=yellow]Source Movies[/COLOR] da luu se bi ghi de.", "Ban co muon tiep tuc?") 
    if y == 0:   
        pass
    else:
        #wizard(name,'https://dl.dropboxusercontent.com/s/jiw6oxgsk34hkf3/ggdrive_library_1.zip',description)
        #wizard(name,'https://dl.dropboxusercontent.com/s/vwoe434v0b927xr/ggdrive_library_2.zip',description)
        wizard("gglibrary",'https://dl.dropboxusercontent.com/s/0btzrhtii3f1n17/ggdrive_library.zip',description)
        dialog.ok("Done!", "Khoi phuc xong, cho Library duoc cap nhat va thuong thuc ^^")
							

def restoreggdrive():
    global analytics
    analytics.sendEvent("Kodi HieuHien.vn", "restore ggdrive")
    y = dialog.yesno("[COLOR red][B]CANH BAO !!![/COLOR][/B]", "Tat ca [COLOR yellow]Account da them vao Google Drive[/COLOR] se bi ghi de.", "Ban co muon tiep tuc?") 
    if y == 0:   
        pass
    else:
        wizard("dataggdrive",'https://dl.dropboxusercontent.com/s/nofqcb6rd9l7v6i/data_ggdrive.zip',description)
        dialog.ok("Done!", "Khoi phuc xong, nhan OK va thuong thuc ^^")
        xbmc.executebuiltin('RunAddon(plugin.googledrive)')		

			
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
setupAnalytics()        
                      
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
        dialog.ok("[COLOR red][B]HieuHien.vn[/B][/COLOR]", '[COLOR yellow]Da cai dat thanh cong![/COLOR]', 'Nhan [B]OK[/B] de thoat Kodi')
        killxbmc()
        
elif mode==2:
        wizard(name,url,description)
        dialog.ok("DONE!", 'Da cai dat xong. Khoi dong lai Kodi de kiem tra.')		
        
		
elif mode==3:
        Tweak()
		
elif mode==4:
        menucache()
		
elif mode==5:
        clearCache()
        dialog.ok("Kodi HieuHien.vn", "Done Clearing Cache files")		
        
elif mode==6:
        deleteThumbnails()
        
elif mode==7:
        purgePackages()
        
elif mode==8:
        clearCache()
        dialog.ok("Kodi HieuHien.vn", "Done Clearing Cache files")	
        purgePackages()
        deleteThumbnails()
        	

elif mode==9:
    global analytics
    analytics.sendEvent("Kodi HieuHien.vn", "view Donate")		
    xbmcaddon.Addon(id='plugin.program.HieuHien.vn').openSettings()
    	
    
    #xbmc.executebuiltin('XBMC.RunPlugin(plugin://plugin.program.HieuHien.vn)')
    #xbmc.executebuiltin('RunAddon(plugin.program.HieuHien.vn)')
elif mode==10:
        restoredata()
        	

elif mode==11:
        restorelibrary()       		

#elif mode==12:
        #restoregdrive()
       		

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
        BACKUP()
        #dialog.ok("Done!", "Khoi phuc xong, nhan OK va thuong thuc ^^")	

elif mode==19:
        RESTORE_ZIP_FILE(name,url)		
		
elif mode==20:
        RESTORE_BACKUP_XML(name,url,description)
		
elif mode==21:
        RESTORE()
		
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))

