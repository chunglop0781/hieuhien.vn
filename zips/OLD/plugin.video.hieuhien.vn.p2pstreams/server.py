import xbmc,xbmcaddon,urllib,urllib2,sys
from resources.core import acestream as ace
from resources.core import sopcast as sop
from resources.core.acecore import TSengine as tsengine
from urlparse import urlparse, parse_qs
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer


currentace = False
currentpvr = False
link = False
linkarray = False
isplay = False
class MyRequestHandler(BaseHTTPRequestHandler):
	
	def do_HEAD(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		self.wfile.write('P2P service is running !')
		self.wfile.close();
		self.finish()
	
	def do_GET(self):
		host = self.headers.get('Host')
		global link
		global currentpvr
		global currentace
		global curmode
		global linkarray
		global isplay
		if self.path == '/':
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('P2P service is running !')
			#self.wfile.close();
			self.finish()
		elif "p2p.m3u?" in self.path:
			args = parse_qs(urlparse(self.path).query);
			url = args['url'][0];
			mode = args['mode'][0];
			EXTM3U = '#EXTM3U\n';
			
			if url == currentace and currentpvr and link:
				isplay = True
				EXTM3U += '#EXT-X-VERSION:3\n'
				EXTM3U += '#EXT-X-ALLOW-CACHE:NO\n'
				EXTM3U += '#EXT-X-TARGETDURATION:16\n'
				EXTM3U += '#EXT-X-MEDIA-SEQUENCE:817\n'
				EXTM3U += '#EXTINF:10.0,\n'
				EXTM3U += link +'\n';
				EXTM3U += '#EXTINF:10.0,\n'
				EXTM3U += link +'\n';	
				EXTM3U += '#EXTINF:10.0,\n'
				EXTM3U += link +'\n\n';
				
				self.send_response(200)
				self.send_header('Content-type',	'application/x-mpegURL')
				self.send_header('Connection',	'close')
				self.send_header('Content-Length', len(EXTM3U))
				self.end_headers()
				self.wfile.write(EXTM3U.encode('utf-8'))
				self.wfile.close()
				self.finish()
			else:
				
				EXTM3U += '#EXTINF:-1, dummy\n'
				EXTM3U += 'blank.mp4\n\n';
				
				self.send_response(200)
				self.send_header('Content-type',	'application/x-mpegURL')
				self.send_header('Connection',	'close')
				self.send_header('Content-Length', len(EXTM3U))
				self.end_headers()
				self.wfile.write(EXTM3U.encode('utf-8'))
				self.wfile.close()
				self.finish()
				try:
					currentpvr = xbmc.Player().getPlayingFile()
					xbmc.Player().stop()
				except: sys.stdout.write('error while stopping play')
				if isplay:
					sys.stdout.write('playing something already, try to stop p2p engine')
					if curmode == '1':
						TSPlayer = tsengine()
						TSPlayer.end()
					elif curmode == '2':
						try:sop.killme(linkarray[1])
						except:sys.stdout.write('Could not stop sopcast !')
					currentace = False
					link = False
					linkarray = False
					alive = 'none'
					curmode = '0'
					xbmc.sleep(1000);
					isplay = False
				currentace = url
				if mode == '1':
					curmode = mode
					link = ace.acestreams('p2pPlay',None,url,True)
					sys.stdout.write('Done get link : %s (%s) (%s)' % (link,currentace,currentpvr))
				elif mode == '2':
					curmode = mode
					linkarray = sop.sopstreams('p2pPlay',None,url,True)
					try:
						link = linkarray[0]
						sys.stdout.write('Done get link : %s (%s) (%s)' % (link,currentace,currentpvr))
					except:sys.stdout.write('Sopcast Failed !')
				if link and len(link) > 5:
					xbmc.sleep(500)
					xbmc.executebuiltin("PlayMedia("+currentpvr+")")
				
			if isplay:
				xbmc.sleep(2000)
				while xbmc.Player().isPlaying() and currentpvr == xbmc.Player().getPlayingFile():xbmc.sleep(2000)
				switchChannel = False
				xbmc.sleep(1000)
				try:
					if 'pvr.iptvsimple' in xbmc.Player().getPlayingFile():switchChannel = True
				except:sys.stdout.write('no channel playing start kill !')
				if not switchChannel:
					if curmode == '1':
						TSPlayer = tsengine()
						TSPlayer.end()
					elif curmode == '2':
						try:sop.killme(linkarray[1])
						except:sys.stdout.write('Could not stop sopcast !')
					currentace = False
					currentpvr = False
					linkarray = False
					link = False
					curmode = '0'
					isplay = False
			
		elif self.path == '/stop':
			if curmode == '1':
				TSPlayer = tsengine()
				TSPlayer.end()
			elif curmode == '2':
				try:sop.killme(linkarray[1])
				except:sys.stdout.write('Could not stop sopcast !')
		else:
			self.send_response(404)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write("404")
			self.wfile.close();

if __name__ == '__main__':

	PORT = 6789
	handler = MyRequestHandler
	httpd = SocketServer.TCPServer(("", PORT), handler)
	sys.stdout.write("p2p web serving at port %d" % PORT)
	httpd.serve_forever()
	sop.break_sopcast()