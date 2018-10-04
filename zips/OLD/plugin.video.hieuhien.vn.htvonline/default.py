# -*- coding: utf-8 -*-

'''
Copyright (C) 2014                                                     

This program is free software: you can redistribute it and/or modify   
it under the terms of the GNU General Public License as published by   
the Free Software Foundation, either version 3 of the License, or      
(at your option) any later version.                                    

This program is distributed in the hope that it will be useful,        
but WITHOUT ANY WARRANTY; without even the implied warranty of         
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
GNU General Public License for more details.                           

You should have received a copy of the GNU General Public License      
along with this program. If not, see <http://www.gnu.org/licenses/>  
'''                                                                           

import urllib,urllib2,re,os,sys,json
import xbmcplugin,xbmcgui,xbmcaddon

addon = xbmcaddon.Addon(id='plugin.video.hieuhien.vn.htvonline')
profile = addon.getAddonInfo('profile')
home = addon.getAddonInfo('path')
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos = xbmc.translatePath(os.path.join(home, 'logos\\'))

def main():
    homeUrl = "http://htvonline.com.vn/livetv"
    content = makeRequest(homeUrl)
    match = re.compile('<a class=.+?data-original="([^"]*)"><img alt=.+?src="([^>]+)"></a>').findall(content)
    for url, thumb in match:
        title = url.split('livetv/')[1]
        name = title.split('-3')[0]
        name = name.replace('-',' ')	  
        addLink( name.upper(), url, 100, thumb)
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.xeebo':
        xbmc.executebuiltin('Container.SetViewMode(52)')  
    else:
        xbmc.executebuiltin('Container.SetViewMode(%d)' % 500)

def resolveUrl(url):
    content = makeRequest(url)
    mediaUrl = re.compile('data-source="(.+?)"').findall(content)[0]
    item=xbmcgui.ListItem(path=mediaUrl)  
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    return
	
def makeRequest(url, headers=None):
    if headers is None:
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                 'Referer' : 'http://www.google.com'}
    try:
        req = urllib2.Request(url,headers=headers)
        f = urllib2.urlopen(req)
        body=f.read()
        return body
    except:
        pass 

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
				  
def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
   
def addLink(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name})
    liz.setProperty('mimetype', 'video/x-msvideo')
    liz.setProperty("IsPlayable","true")
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
    return ok  
  
params=get_params()
url=None
name=None
mode=None
iconimage=None

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass  
try:mode=int(params["mode"])
except:pass

sysarg=str(sys.argv[1])

if mode==None or url==None or len(url)<1:
   main()

elif mode==100:
     dialogWait = xbmcgui.DialogProgress()
     dialogWait.create('Đang tải. Vui lòng chờ trong giây lát...')
     resolveUrl(url)
     dialogWait.close()
     del dialogWait
	 
xbmcplugin.endOfDirectory(int(sys.argv[1]))