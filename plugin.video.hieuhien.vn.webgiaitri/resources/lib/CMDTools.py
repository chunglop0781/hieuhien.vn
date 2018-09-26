import xbmcaddon
import thread, threading
import urllib, urllib2
import datetime, time
import xbmc

def get_path_img(path):
	img_path = 'special://home/addons/'+xbmcaddon.Addon().getAddonInfo('id')+'/'+path
	return img_path
def build_url(base_url,query):
    return base_url + '?' + urllib.urlencode(query)
def download_list_image(urls, path):
	threads=[]
	for url in urls:
		fn=datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')+".jpg"
		th = threading.Thread(target=download, args=(url,path+fn,))
		th.start()
		threads.append(th)
		#thread.start_new_thread(download, (url,path+fn,))
	xbmc.log ("Waiting...")

	for th in threads:
		xbmc.log(str(threading.activeCount()))
		th.join()
		
	xbmc.log("Complete.")
	return
def download(url, pathfile):
	try:
		u = urllib2.urlopen(url)
		f = open(pathfile, 'wb')

		file_size_dl = 0
		block_sz = 8192
		while True:
			buffer = u.read(block_sz)
			if not buffer:
				break
			file_size_dl += len(buffer)
			f.write(buffer)
			#status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
			#status = status + chr(8)*(len(status)+1)
			#print str(file_size_dl)
		f.close()
	except:			
		xbmc.log("__Sleep___")