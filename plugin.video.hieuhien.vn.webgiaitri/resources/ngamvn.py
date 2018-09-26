import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc
import requests
from bs4 import BeautifulSoup
from lib import CMDTools

base_url = sys.argv[0]
web_name="NGAMVN.COM"
web_url = "http://www.ngamvn.com/" 

def get_Web_Name():
	return web_name

def get_img_thumb_url():
	return CMDTools.get_path_img('resources/media/ngamvn.png')

def view():
	catalogues=[{'label':'Clip','id':'clip'},
				{'label':'Home','id':'home'},
				{'label':"\x4D\xE1\xBB\x9B\x69\x20\x6E\x68\xE1\xBA\xA5\x74".decode('utf-8'),'id':'moi'},
				{'label':'\x4B\x68\x61\x63'.decode('utf-8'),'id':'khac'},
				{'label':'\xE1\xBA\xA2\x6E\x68\x20\xC4\x91\x61\x6E\x67\x20\x68\x6F\x74'.decode('utf-8'),'id':'hot'},
				{'cat':'anh-vui-anh-che','label':'\xE1\xBA\xA2\x6E\x68\x20\x56\x75\x69\x20\x2D\x20\xE1\xBA\xA2\x6E\x68\x20\x43\x68\xE1\xBA\xBF'.decode('utf-8'),'id':'anh-vui-anh-che'},
				{'label':'\xE1\xBA\xA2\x6E\x68\x20\x47\x69\x72\x6C'.decode('utf-8'),'id':'anh-girl'}]

	addon_handle = int(sys.argv[1])
	addon       = xbmcaddon.Addon()
	addonname   = addon.getAddonInfo('name')
	
	args = urlparse.parse_qs(sys.argv[2][1:])

	xbmcplugin.setContent(addon_handle, 'movies')

	#cat: catalog
	#page: So thu tu page
	#url: Dia chi trang web
	cat = args.get('cat', None)
	mode = args.get('mode', None)
	page = args.get('page', None)
	urlLink = args.get('url', None)

	url=web_url

	#Neu click vao link play
	if urlLink != None:
		response = requests.get(urlLink[0])
		html = response.text
		soup = BeautifulSoup(html)
		imgDiv=soup.find("meta", attrs = {"property":"og:image"})
		src=imgDiv.get("content")
		if src.startswith('http://img.youtube.com'):
			src=src.split('/')[-2]
			xbmc.Player().play("plugin://plugin.video.youtube/play/?video_id="+src)
		else:
			imgSrc=src
			xbmc.executebuiltin('ShowPicture('+imgSrc+')')
		return

	#Neu vao trang chon muc
	if cat==None:
		for c in catalogues:
			li = xbmcgui.ListItem(c['label'])
			urlList = CMDTools.build_url(base_url,{'web':get_Web_Name(), 'cat':c['id']})
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=urlList, listitem=li, isFolder=True)
		return
	#Load noi dung trang
	else:
		#Dat url trang
		if page != None:
			page=int(page[0])
		else: 
			page=1
		url=web_url+cat[0].replace('home','')+'?page='+str(page)
		#Load noi dung
		response = requests.get(url)
		html = response.text
		soup = BeautifulSoup(html)
		divImgs=soup.findAll("div", attrs = {"class":"center"})
		#Tao list Item
		for divItem in divImgs:
			url_Item_Link="http://www.ngamvn.com"+divItem.find("a").get("href")
			url_Item_Thumb=divItem.find("img", attrs = {"class":"thumb"}).get("src")
			url_Item_Label=divItem.find("a", attrs = {"target":"_blank"}).get_text().lstrip()
			if url_Item_Link!=None and url_Item_Thumb!=None:
				if(url_Item_Thumb.startswith("http://")!=True):
					if (url_Item_Thumb.startswith("https://")==True):
						url_Item_Thumb=url_Item_Thumb
					else:
						url_Item_Thumb=web_url+url_Item_Thumb
				li = xbmcgui.ListItem(url_Item_Label.encode('utf-8'))
				li.setThumbnailImage(url_Item_Thumb)
				urlList=CMDTools.build_url(base_url,{'web':web_name,'url': url_Item_Link.encode('utf-8')});
				xbmcplugin.addDirectoryItem(handle=addon_handle , url=urlList, listitem=li)
		#Tao nut next
		li = xbmcgui.ListItem("Next")
		urlList=CMDTools.build_url(base_url,{'web':web_name, 'cat':cat[0],'page': page+1});
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=urlList, listitem=li, isFolder=True)