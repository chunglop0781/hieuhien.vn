# -*- coding: utf-8 -*-
__author__ = 'thaitni'
import json
from utils import xread, xrw, mess, u2s

class fshare:
	def __init__(self, user, passwd):
		self.user   = user
		self.passwd = passwd
		cookie = xrw('newfshare.cookie').split('-')
		
		try:
			self.session_id = cookie[0]
			self.token      = cookie[1]
		except:
			self.session_id = ""
			self.token      = ""
		
		try    : self.acc = cookie[2]
		except : self.acc = ""
		
		try    : self.key  = cookie[3]
		except : self.key  = ""
		
		self.hd = {'Cookie' : 'session_id=' + self.session_id}
		
	def results(self, url, hd = {'User-Agent':'Mozilla/5.0'}, data = None):
		try   :  j = json.loads( xread(url, hd, data) )
		except : j = {}
		return j
	
	def vip(self, session_id):
		hd = {'Cookie' : 'session_id=' + session_id}
		userInf = self.results("https://api2.fshare.vn/api/user/get", hd)
		if userInf.get("account_type", "") == "Bundle":
			vip = 1
		else:
			try    : vip = int(userInf.get("expire_vip","-1"))
			except : vip = -1
			if vip > 0: 
				from time import time
				vip = 1 if time() < vip else -1
		return  vip >= 0
	
	def login(self, user, passwd):
		data   = '{"app_key" : "%s", "user_email" : "%s", "password" : "%s"}'
		data   = data % (self.key, user, passwd)
		result = self.results("https://api2.fshare.vn/api/user/login", data = data)
		
		if result.get("code", 0) == 200:
			if self.vip( result.get("session_id") ):
				self.session_id  = result.get("session_id")
				self.token       = result.get("token")
				self.hd          = {'Cookie' : 'session_id=' + self.session_id}
				xrw('newfshare.cookie', self.session_id + "-" + self.token + "--" + self.key)
				mess( "Login thành công", "Fshare.vn")
				
			else:
				mess( "Acc của bạn hết hạn VIP", "Fshare.vn")
		else:
			mess( "Login không thành công!", "Fshare.vn")

	def getLink(self, url, passwd = ""):
		if not self.session_id:
			self.login(self.user, self.passwd)
			if not self.session_id:
				return ""
		elif not self.vip(self.session_id):
			return ""
		
		data   = '{"token" : "%s", "url" : "%s", "password" : "%s"}'
		data   = data % (self.token, url, passwd)
		result = self.results("https://api2.fshare.vn/api/session/download", self.hd, data)
		
		link = ""
		if result.get("location"):
			link = result.get("location")
		
		elif result.get("code", 0) == 123 and not passwd:
			from utils import get_input
			passwd = get_input(u'Hãy nhập: Mật khẩu tập tin')
			if passwd:
				link = self.getLink(url, passwd)
		
		if not link:
			link = "Failed"
		elif link and self.acc:
			self.thanks(u2s(self.acc))
		
		return link
	
	def thanks(self, acc):
		mess("Cảm ơn: [COLOR cyan]%s[/COLOR] đã hỗ trợ xem phim này" % acc)
	
	def getToken(self):
		from utils import addon
		return addon.getAddonInfo("name")
	
	def getLinkFree(self, url):
		from utils import xget
		import urllib
		data = urllib.urlencode({"url" : url, "token" : self.getToken()})
		b    = xget('http://ycofo.xyz/fshare.php', data=data)
		if not b:
			b = xget('http://xshare.eu5.org/fshare.php', data=data)
		
		if b : 
			try    : j = json.loads(b.read())
			except : j = {}
		else : j = {}
		
		if j.get("msg"):
			mess(j.get("msg"))
		
		link = j.get("location", "")
	
		if link == "Copy":
			mess("Đây là bản copy của [COLOR red][B]Xshare[/COLOR] [COLOR green]XBMC[/COLOR] [COLOR blue]HDVideo[/B][/COLOR]")
			link = ""
		elif link:
			self.acc = j.get("user","")
			if j.get("session_id") and j.get("token"):
				data = u2s(j.get("session_id")+"-"+j.get("token")+"-"+self.acc+"-"+j.get("key", ""))
				xrw('newfshare.cookie', data)
			
			if self.acc:
				self.thanks(u2s(self.acc))
		
		return link

def kphim(b, url, server_id, video_id):
	hd  = {
		'User-Agent'       : 'Mozilla/5.0',
		'X-Requested-With' : 'XMLHttpRequest',
		'Referer'          : url
	}
	from hashlib import md5
	from utils import xsearch
	ver  = xsearch("ver\W*'(.+?)'",b)
	tk   = "kp" + server_id + "dung_get_em_nua" + video_id  + ver
	tk   =	md5(tk).hexdigest()[1:]
	href = "http://www.kphim.tv/player/%s/%s/%s" % (server_id + ver, video_id + ver, tk)
	data = 'mid=%s&vid=%s&sid=%s'%(ver,server_id,video_id)
	#import xbmc;xbmc.log("b=xread('%s',%s,'%s')"%(href,str(hd),data))
	return xread(href,hd,data)

def getToken(server_id, video_id, ver):
	#http://kphim.tv/resources/js/site.js?ver=37 mahoahkphim
	from hashlib import md5
	tk   = "kp" + server_id + "dung_get_em_nua" + video_id  + ver
	tk   =	md5(tk).hexdigest()[1:]
	href = "http://www.kphim.tv/player/%s/%s/%s" % (server_id + ver, video_id + ver, tk)
	return href

def getLinkTVhay(url):
	return ""

def phimnhanh(b):
	href=xsearch('link_url.+?(http.+?)"',b).replace("\\","") + xsearch('"key\W+"(.+?)"',b)
	try    : j = json.loads(xread(href))
	except : j = {}
	return j