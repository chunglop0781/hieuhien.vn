import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import json, re, sys, urllib, urlparse

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
fanart      = addon.getAddonInfo('path') + '/fanart.jpg'

args = urlparse.parse_qs(sys.argv[2][1:])

#Sets content type (files, songs, artists, albums, movies, tvshows, episodes, musicvideos)
xbmcplugin.setContent(addon_handle, 'Video')

def build_url(query):
	return base_url + '?' + urllib.urlencode(query)

#Autofetches thumbs; Slow; Consider caching to a PHP server
def get_thumb(id):
	try:
		yt = urllib.urlopen('https://www.youtube.com/'+id).read(7000)
		thumb = re.findall('<link rel="image_src" href="(.+?)">', yt)[0]
		thumb = thumb.replace('/s900','/s300') #Reduce image size
		thumb = thumb.replace('//i.ytimg.com','https://i.ytimg.com') #Clean up URL
	except:
		return ''
	else:
		return thumb

mode = args.get('mode', None)

#Web based list:
url = "https://github.com/hieuhienvn/hieuhien.vn/raw/master/plugin.video.viettube.channels.json"
response = urllib.urlopen(url);
data = json.loads(response.read())
xbmc.log(str(data["catalogues"]))

#File based list:
#file = addon.getAddonInfo('path') + '/plugin.video.viettube.channels.json'
#f = open (file, 'r')
#data = json.loads(f.read())
#f.close()
#xbmc.log(str(data["catalogues"]))

if mode is None:
	skin_used = xbmc.getSkinDir()
	if skin_used == 'skin.heidi':
		xbmc.executebuiltin('Container.SetViewMode(53)')
	elif skin_used == 'skin.confluence':
		xbmc.executebuiltin('Container.SetViewMode(500)')

	for cat in data["catalogues"]:
		foldername=cat["name"].encode('utf-8')
		xbmc.log(cat["name"].encode('utf-8'))
		url = build_url({'mode': 'folder', 'foldername': foldername, "id":str(cat["id"])})
		thumb=cat["thumb"]
		li = xbmcgui.ListItem(foldername, iconImage=thumb, thumbnailImage=thumb); li.setProperty('Fanart_Image', fanart)
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

	xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'folder':
	skin_used = xbmc.getSkinDir()
	if skin_used == 'skin.heidi':
		xbmc.executebuiltin('Container.SetViewMode(53)')
	elif skin_used == 'skin.confluence':
		xbmc.executebuiltin('Container.SetViewMode(500)')

	id=int(args.get('id', None)[0])
	for chan in data["catalogues"][id]["channels"]:
		xbmc.log("chan:"+str(chan))
		xbmc.log("chan ID:"+chan["id"])
		url = "plugin://plugin.video.youtube/"+chan["id"].encode('utf-8')

#		thumb = get_thumb(chan["id"]) #Web fetched
#			if not thumb == '': #indent section below this line

		thumb = chan["thumb"] #JSON stored
		li = xbmcgui.ListItem(chan["name"].encode('utf-8'), iconImage=thumb, thumbnailImage=thumb); li.setProperty('Fanart_Image', fanart)
		li.setProperty('isplayable', 'true')
		xbmcplugin.addDirectoryItem(handle=addon_handle , url=url, listitem=li, isFolder=True)

	xbmcplugin.endOfDirectory(addon_handle)