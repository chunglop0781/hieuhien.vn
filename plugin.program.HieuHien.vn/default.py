##################################################################################
#                          THANK!
# Addon nay duoc tong hop tu internet va co su dung code tu addon raw.maintenance.
##################################################################################
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


USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base='https://HieuHien.vn'
ADDON=xbmcaddon.Addon(id='plugin.program.HieuHien.vn')
dialog = xbmcgui.Dialog()    
VERSION = "1.0.0"
PATH = "HieuHien.vn"            

thumbnailPath = xbmc.translatePath('special://thumbnails');
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath = xbmc.translatePath('special://temp')
addonPath = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.program.HieuHien.vn')
mediaPath = os.path.join(addonPath, 'media')
databasePath = xbmc.translatePath('special://database')


#######################################################################
#                          CLASSES
#######################################################################

class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi
     
def CATEGORIES():
    #setView('movies', 'MAIN')
    xbmc.executebuiltin("Container.SetViewMode(500)")	    	
    addDir1('Cai dat KODI','url', 14,os.path.join(mediaPath, "data.jpg"))
    addDir1('Thay doi giao dien','url', 15,os.path.join(mediaPath, "skin.jpg"))	
    addDir1('AdvancedSetting.xml','url', 3,os.path.join(mediaPath, "buffer.jpg"))
    addDir1('Cap nhat','url', 16,os.path.join(mediaPath, "update.jpg"))
    addDir1('Clear cache','url', 4,os.path.join(mediaPath, "clean.jpg"))
    addDir1('About','url', 9,os.path.join(mediaPath, "about.jpg"))

def Data():
    link = OPEN_URL('https://dl.dropboxusercontent.com/s/nvngs5c4fie18s6/KodiVersion.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,2,iconimage,fanart,description)
    xbmc.executebuiltin("Container.SetViewMode(500)")	    

def Update():
	#link = OPEN_URL('https://dl.dropboxusercontent.com/s/x2waef04tt5aw9b/Capnhat.txt').replace('\n','').replace('\r','')
    link = OPEN_URL('https://dl.dropboxusercontent.com/s/x2waef04tt5aw9b/Capnhat.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,2,iconimage,fanart,description)
    xbmc.executebuiltin("Container.SetViewMode(500)")	    

def Skin():
    link = OPEN_URL('https://dl.dropboxusercontent.com/s/3sri9c3v512dk8i/Giaodien.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,2,iconimage,fanart,description)
    xbmc.executebuiltin("Container.SetViewMode(500)")	    

def restoredata():
    xbmc.executebuiltin("Container.SetViewMode(500)")
    addItem('Restore Movies Library - Danh cho Addon: gdrive & Google Drive','url', 11,os.path.join(mediaPath, "movieslibrary.png"))
    addItem('Data Addon Gdrive', 'url', 12,os.path.join(mediaPath, "gdrive.png"))
    addItem('Data  Addon Google Drive', 'url', 13,os.path.join(mediaPath, "ggdrive.png"))
	
def Buffer():
    link = OPEN_URL('https://dl.dropboxusercontent.com/s/kx45j8cmbl2rfcb/buffer.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,2,iconimage,fanart,description)
    xbmc.executebuiltin("Container.SetViewMode(500)")	

    
def menucache():
    #analytics.sendPageView("RawMaintenenance","maintenance","maint")
    xbmc.executebuiltin("Container.SetViewMode(500)")
    addItem('Xoa Cache - Clear Cache','url', 5,os.path.join(mediaPath, "clearcache.jpg"))
    addItem('Xoa Anh Thu Nho Video - Delete Thumbnails', 'url', 6,os.path.join(mediaPath, "clearthumbnail.jpg"))
    addItem('Xoa Goi Cai Dat Cu - Purge Packages', 'url', 7,os.path.join(mediaPath, "clearpackage.jpg"))
    addItem('[COLOR red][B]Xoa Tat Ca Rac - Delete All[/B][/COLOR]', 'url', 8,os.path.join(mediaPath, "deleteall.jpg"))	

    
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
def wizard(name,url,description):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR red][B]HienHien.vn[/B][/COLOR]","[B][COLOR red]Buoc 1:[/COLOR] Dang tai file cai dat...[/B]",'', "[B]Cho 1 chut nha!!![/B]")
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "[B][COLOR red]Buoc 2: [/COLOR]Dang giai nen file....[/B]")
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
    choice = xbmcgui.Dialog().yesno('[COLOR red][B]Kodi Exit!![/B][/COLOR]', '[COLOR red][B]KHONG DUNG[/B][/COLOR] chuc nang [B]Quit/Exit[/B] trong Kodi. Neu cua so KODI khong tat hay Khoi dong lai thiet bi', nolabel='Khong, huy bo!',yeslabel='Ok, thoat!')
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
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "KODI khong tu tat duoc", "[COLOR=yellow][B]Ban phai[/COLOR][/B] tu tat ung dung Kodi thu cong.","Neu khong tat duoc thi khoi dong lai may.",'')
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
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "KODI khong tu tat duoc", "[COLOR=yellow][B]Ban phai[/COLOR][/B] tu tat ung dung Kodi thu cong.","Neu khong tat duoc thi khoi dong lai may.",'')
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
        dialog.ok("[COLOR=red][B]WARNING  !!![/B][/COLOR]", "Ban dang su dung thiet bi Android ", "[COLOR=yellow][B]Ban phai[/COLOR][/B] tu tat ung dung Kodi thu cong.","Neu khong tat duoc hay khoi dong lai may.","[COLOR red][B]KHONG DUNG[/B][/COLOR] chuc nang [B]Quit/Exit[/B] trong Kodi.")
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
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Neu ban thay tin nhan nay nghia la KODI ko tu tat duoc", "[COLOR=lime]Khong tat[/COLOR] KODI bang Menu Exit.","Dung Task Manager de tat va khong dung ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "KODI khong tu tat duoc", "[COLOR=yellow][B]Ban phai[/COLOR][/B] tu tat ung dung Kodi thu cong.","Neu khong tat duoc thi khoi dong lai may.")    

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
    #global analytics
    #analytics.sendEvent("Maintenance", "ClearCache")
    
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
    dialog.ok("HieuHien.vn - Clear cache", "Da xoa cache xong!")
    
    
def deleteThumbnails():
    #global analytics
    #analytics.sendEvent("Maintenance", "DeleteThumbnails")
    
    if os.path.exists(thumbnailPath)==True:  
            dialog = xbmcgui.Dialog()
            if dialog.yesno("HieuHien.vn - Delete Thumbnails", "Ban co muon xoa thumbnail khong?"):
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
    #global analytics
    #analytics.sendEvent("Maintenance", "PurgePacakges")
    
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
                dialog.ok("HieuHien.vn - Xoa tap tin cu", "Da xoa toan bo tap tin cu!")
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok("HieuHien.vn - Delete packages", "Hien tai khong co tap tin cu nao trong may!")       

def restorelibrary():
    y = dialog.yesno("[COLOR red][B]CANH BAO !!![/COLOR][/B]", "Thu vien phim chi Play voi Data Account cai dat tu HieuiT Wizard","Tat ca [COLOR=yellow]Source Movies[/COLOR] da luu se bi ghi de.", "Ban co muon tiep tuc?") 
    if y == 0:   
        pass
    else:
        wizard("gglibrary",'https://dl.dropboxusercontent.com/s/0btzrhtii3f1n17/ggdrive_library.zip',description)
        dialog.ok("Done!", "Khoi phuc xong, cho Library duoc cap nhat va thuong thuc ^^")
						
def restoregdrive():
    y = dialog.yesno("[COLOR red][B]CANH BAO !!![/COLOR][/B]", "Tat ca [COLOR yellow]Account da them vao Gdrive[/COLOR] se bi ghi de.", '', "Ban co muuon tiep tuc?") 
    if y == 0:   
        pass
    else:
        wizard("datagdrive",'https://dl.dropboxusercontent.com/s/82w2elvg2t2kood/data_gdrive.zip',description)
        dialog.ok("Done!", "Khoi phuc xong, nhan OK va thuong thuc ^^")
        #xbmc.executebuiltin('RunAddon(plugin.video.gdrive)')		

def restoreggdrive():
    y = dialog.yesno("[COLOR red][B]CANH BAO !!![/COLOR][/B]", "Tat ca [COLOR yellow]Account da them vao Google Drive[/COLOR] se bi ghi de.", "Ban co muon tiep tuc?") 
    if y == 0:   
        pass
    else:
        wizard("dataggdrive",'https://dl.dropboxusercontent.com/s/o428ctuabklzw1j/HieuHienKODI.zip',description)
        dialog.ok("Done!", "Khoi phuc xong, nhan OK va thuong thuc ^^")
        #xbmc.executebuiltin('RunAddon(plugin.googledrive)')		
		
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
        CATEGORIES()
       
elif mode==1:
        wizard(name,url,description)
        dialog.ok("[COLOR red][B]HieuHien.vn[/B][/COLOR]", '[COLOR yellow]Da cai dat thanh cong![/COLOR]', 'Nhan [B]OK[/B] de thoat Kodi')
        killxbmc()
        
elif mode==2:
        wizard(name,url,description)
        dialog.ok("DONE!", 'Da cai dat xong. Vui long khoi dong lai KODI de su dung!')		
        killxbmc()
		
elif mode==3:
        Buffer()
		
elif mode==4:
        menucache()
		
elif mode==5:
        clearCache()
        
elif mode==6:
        deleteThumbnails()
        
elif mode==7:
        purgePackages()
        
elif mode==8:
        clearCache()
        purgePackages()
        deleteThumbnails()

elif mode==9:		
    xbmcaddon.Addon(id='plugin.program.HieuHien.vn').openSettings()
    
elif mode==10:
        restoredata()
        	

elif mode==11:
        restorelibrary()       		

elif mode==12:
        restoregdrive()
       		

elif mode==13:
        restoreggdrive()

elif mode==14:
        Data()

elif mode==15:
        Skin()

elif mode==16:
        Update()
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))

