# -*- coding: utf-8 -*-

import urllib, urlparse, xbmc, xbmcgui, xbmcplugin, xbmcaddon, sys, os, json

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo("name")
home = addon.getAddonInfo("path")
logos = xbmc.translatePath(os.path.join(home, "resources", "logos"))

args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, "movies")

def build_url(query):
    return base_url + "?" + urllib.urlencode(query)

mode = args.get("mode", None)

dataFile = open(xbmc.translatePath(os.path.join(home, "data.json")))
data = json.loads(dataFile.read())
dataFile.close()

if mode is None:
    for mainmenu in data["channels"]:
        foldername =  mainmenu["name"].encode("utf-8")
        url = build_url({"mode": "folder", "foldername": foldername, "chan": str(mainmenu["channel"])})      
        li = xbmcgui.ListItem(foldername, iconImage = logos + "/" + mainmenu["thumb"])
        xbmcplugin.addDirectoryItem(handle = addon_handle, url = url, listitem = li, isFolder = True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == "folder":
    item = int(args.get("chan", None)[0])
    for submenu in data["channels"][item]["items"]:
        if "youtube" in submenu["link"]:
            url = "plugin://plugin.video.%s" % submenu["link"]
        else:
            url = "plugin://plugin.video.dailymotion_com/?mode=sortVideos1&url=owner:" + submenu["link"] 
        li = xbmcgui.ListItem(submenu["title"].encode("utf-8"), iconImage = submenu["thumb"])       
        li.setProperty("isplayable", "true")
        xbmcplugin.addDirectoryItem(handle = addon_handle, url = url, listitem = li, isFolder = True)
    xbmcplugin.endOfDirectory(addon_handle)