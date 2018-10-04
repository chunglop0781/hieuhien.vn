import time
import xbmc
import urlparse
import SimpleHTTPServer
import SocketServer
import urllib2
import urllib
import re
import json
import base64

def remove_special_chars(str):
	pattern = re.compile('[\W_]+')
	return pattern.sub('', str)

# Channel class
class Channel:
	def __init__(self, name, source, original_url):
		self.name = name
		self.source = source
		self.original_url = original_url

class ChannelService:
	channels = {}
	regex = {}

	# update channels list
	def updateChannels(self):
		request = urllib2.urlopen('http://goo.gl/91eFwY')
		htmlStr = request.read()
		request.close()

		lines = htmlStr.splitlines()
		i = 0
		while i < len(lines):
			ch = Channel(remove_special_chars(lines[i]), remove_special_chars(lines[i+1]), lines[i+2])
			i+= 3
			ChannelService.channels[ch.name] = ch

	# update regex list
	def updateRegex(self):
		request = urllib2.urlopen('http://goo.gl/MeHSkW')
		htmlStr = request.read()
		request.close()

		lines = htmlStr.splitlines()
		i = 0
		while i < len(lines):
			ChannelService.regex[remove_special_chars(lines[i])] = lines[i+1]
			i+= 2

	# decode to get session id
	def decodeVTVPlusLink (self, key ,enc):
		tempStr = []
		enc = base64.urlsafe_b64decode(enc)

		for i in range (len(enc)):
			oldChar = key[i % len(key)]
			newChar = chr((256 + ord(enc[i]) - ord(oldChar)) % 256)
			tempStr.append(newChar)

		return "".join(tempStr)

	# get video stream from original url
	def getStreamURL(self, ch):
		if ch.source in ChannelService.regex:
			htmlStr = urllib2.urlopen(ch.original_url).read()
			p = re.compile(ChannelService.regex[ch.source])
			m = p.search(htmlStr)
			if (m):
				return urllib.unquote(m.group(1)).decode('utf8')
		return ""

# Handle HTTP request
class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	channel_service = ChannelService()

	def do_HEAD(self):
		self.do_GET()

	def do_GET(self):
		if self.path == '/':
			dummy_response = 'Viet IPTV Service'
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(dummy_response)
			self.wfile.close();
		else:
			parsed_params = urlparse.urlparse(self.path)
			parsed_queries = urlparse.parse_qs(parsed_params.query)

			if parsed_params.path == '/channel':
				if (("id" in parsed_queries) and (parsed_queries["id"][0] in ChannelService.channels)):
					dummy_response = MyRequestHandler.channel_service.getStreamURL(ChannelService.channels[parsed_queries["id"][0]])
					self.send_response(301)
					self.send_header('Content-type','text/html')
					self.send_header('Location', dummy_response)
					self.end_headers()
				else:
					dummy_response = "Can't not find channel"
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()
					self.wfile.write(dummy_response)
					self.wfile.close();
			elif parsed_params.path == '/update':
				channel_service = ChannelService()
				channel_service.updateChannels()
				channel_service.updateRegex()
				sys.stdout.write("Channels list are updated")
			else:
				self.send_response(404)
				self.send_header('Content-type','text/html')
				self.end_headers()
				self.wfile.write("404")
				self.wfile.close();

	def log_request(self, code='-', size='-'):
		sys.stdout.write("%s %s %s" % (self.requestline, str(code), str(size)))

if __name__ == '__main__':

	channel_service = ChannelService()
	channel_service.updateChannels()
	channel_service.updateRegex()

	PORT = 9999
	handler = MyRequestHandler
	httpd = SocketServer.TCPServer(("", PORT), handler)
	sys.stdout.write("serving at port %d" % PORT)
	httpd.serve_forever()